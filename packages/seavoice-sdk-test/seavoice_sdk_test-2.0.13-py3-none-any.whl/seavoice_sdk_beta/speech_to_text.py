# -*- coding: utf-8 -*-

"""
SeaVoice Speech SDK v2

Descriptions:
To connect to SeaVoice STT server to finish speech recognizing and synthesizing work.
"""

import asyncio
import contextlib
import json
import logging
from types import TracebackType
from typing import AsyncIterator, Optional, Type, TypeVar, Union

from typing_extensions import ParamSpec
from websockets.legacy.client import WebSocketClientProtocol

from seavoice_sdk_beta.commands import (
    AudioDataCommand,
    BaseCommand,
    LanguageCode,
    SpeechRecognitionAuthenticationCommand,
    SpeechRecognitionAuthenticationPayload,
    SpeechRecognitionSetting,
    StopCommand,
    MultiCommands
)
from seavoice_sdk_beta.events import (
    BaseEvent,
    InfoEvent,
    RecognizedEvent,
    RecognizingEvent,
    SpeechStatus,
    raw_data_to_event,
)
from seavoice_sdk_beta.exceptions import AuthenticationFail, ClosedException, SeavoiceException, UnExpectedClosedException
from seavoice_sdk_beta.logger import default_logger
from seavoice_sdk_beta.utils import get_task_result, get_wrapped_ws, wait_task_result

RT = TypeVar("RT")
Param = ParamSpec("Param")

DEFAULT_STT_ENDPOINT_URL = "wss://seavoice.seasalt.ai/api/v1/stt/ws"
RECEIVE_EVENT_TIMEOUT = 1800


class SpeechRecognizer:
    def __init__(
        self,
        token: str,
        language: LanguageCode,
        sample_rate: int,
        sample_width: int,
        contexts: Optional[dict] = None,
        context_score: int = 0,
        enable_itn: bool = True,
        enable_punctuation: bool = True,
        stt_endpoint_url: str = DEFAULT_STT_ENDPOINT_URL,
        logger: Optional[logging.Logger] = None,
        stt_server_id: Optional[str] = None,
        send_chunk_interval: float = 0.05,
        retry_max: int = 3,
    ) -> None:
        self.token = token
        self.language = language
        self.sample_rate = sample_rate
        self.sample_width = sample_width
        self.channel = 1
        self.enable_itn = enable_itn
        self.enable_punctuation = enable_punctuation
        self.contexts = contexts
        self.context_score = context_score
        self.stt_server_id = stt_server_id
        self.logger = logger or default_logger

        self.send_chunk_interval = send_chunk_interval
        self.retry_max = retry_max
        self.retry_count = 0
        self.connection_count = 0

        self._last_exec: BaseException
        self._error_raised = asyncio.Event()

        self.ws_endpoint_url = stt_endpoint_url
        self.websocket: WebSocketClientProtocol
        self._send_task: asyncio.Task[None]
        self._send_queue = asyncio.Queue()
        self._recv_task: asyncio.Task[None]
        self._recv_queue = asyncio.Queue()
        self._bg_handler: asyncio.Task[None]
        self._bg_command_queue = asyncio.Queue()

        self._segment_id_offset: int = 0
        self._recv_segment_id: int = 0
        self._sent_bytes: int = 0
        self._voice_start_offset: float = 0

        self._base_sleep_time = 2
        self._max_sleep_time = 30

    @property
    def chunk_size(self) -> int:
        return int(self.sample_rate * self.sample_width * self.channel * self.send_chunk_interval)

    def update_recognition_status(self) -> None:
        self._voice_start_offset = self._sent_bytes / (self.sample_rate * self.sample_width * self.channel)
        self._sent_bytes = 0
        self._segment_id_offset = self._recv_segment_id + 1
        self._recv_segment_id = 0

    async def __aenter__(self) -> "SpeechRecognizer":
        await self._init_connection()
        self._send_task = asyncio.create_task(self._send_from_queue())
        self._recv_task = asyncio.create_task(self._recv_to_queue())
        self._bg_handler = asyncio.create_task(self._handle_bg_and_ws())
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        await self.close()
        self._error_raised = asyncio.Event()
        self.retry_count = 0
        self.connection_count = 0

        self._segment_id_offset = 0
        self._recv_segment_id = 0
        self._sent_bytes = 0
        self._voice_start_offset = 0
        return (exc_type == ClosedException) or (exc_type is None)

    async def close(self):
        self._bg_handler.cancel()
        self._send_task.cancel()
        self._recv_task.cancel()
        await self._force_close_ws()
        if self._error_raised.is_set():
            del self._last_exec

    async def _init_connection(self):
        base_sleep_time = self._base_sleep_time
        while True:
            try:
                self.logger.info(f"speech-to-text: {id(self)}-{self.connection_count + 1} start")
                self.websocket = await get_wrapped_ws(self.ws_endpoint_url)
                self.connection_count += 1
                await self._authentication()
                self.logger.info(f"speech-to-text: {id(self)}-{self.connection_count} finish")
                return
            except UnExpectedClosedException as error:
                if self.retry_count > self.retry_max:
                    self.logger.error(
                        f"speech-to-text: {id(self)}-{self.connection_count} has too many UnExpectedClosedException"
                    )
                    raise error

                self.retry_count += 1
                self.logger.info(
                    f"speech-to-text: {id(self)}-{self.connection_count + 1} should retry after {base_sleep_time} sec"
                )
                await asyncio.sleep(base_sleep_time)
                base_sleep_time = min(base_sleep_time * 2, self._max_sleep_time)
            except BaseException as error:
                self.logger.error(f"speech-to-text: {id(self)}-{self.connection_count + 1} raise {error}")
                raise error

    async def _handle_bg_and_ws(self):
        while True:
            reconnect = asyncio.create_task(self._bg_command_queue.get())
            await asyncio.wait([self._send_task, self._recv_task, reconnect], return_when=asyncio.FIRST_COMPLETED)
            reconnect_done = reconnect.result() if reconnect.done() else None
            try:
                if reconnect_done:
                    await self._soft_close_bg_when_working()
                else:
                    reconnect.cancel()
                    await self._soft_close_bg_when_error()  # may raise error

                await self._force_close_ws()
                self.update_recognition_status()
                await self._init_connection()  # may raise error
            except BaseException as error:
                self._last_exec = error
                self._error_raised.set()

            if isinstance(reconnect_done, asyncio.Event):
                reconnect_done.set()

            if self._error_raised.is_set():
                self.logger.info(
                    f"speech-to-text: {id(self)}-{self.connection_count} close because "
                    f"_init_connection raise {self._last_exec}"
                )
                self._send_task.cancel()
                self._recv_task.cancel()
                return

            self._send_task = asyncio.create_task(self._send_from_queue())
            self._recv_task = asyncio.create_task(self._recv_to_queue())

    async def _soft_close_bg_when_error(self):
        send_exec = get_task_result(self._send_task)
        recv_exec = get_task_result(self._recv_task)

        self.logger.info(
            f"speech-to-text: {id(self)}-{self.connection_count} got "
            f"send_task exception: {send_exec} recv_task exception: {recv_exec}"
        )
        # stop if there is an non unexpected exception
        if not (isinstance(recv_exec, UnExpectedClosedException) or isinstance(send_exec, UnExpectedClosedException)):
            self.logger.info(f"speech-to-text: {id(self)}-{self.connection_count} close due to {recv_exec} or {send_exec}")
            last_exec = recv_exec or send_exec
            assert last_exec is not None
            raise last_exec

        if not self._recv_task.done():
            self.logger.info(
                f"speech-to-text: {id(self)}-{self.connection_count} wait recv_task done because "
                "UnExpectedClosedException from send_task means recv_task is going to stop"
            )
            await wait_task_result(self._recv_task)
        if not self._send_task.done():
            self.logger.debug(
                f"speech-to-text: {id(self)}-{self.connection_count} wait send_task done because "
                "UnExpectedClosedException from recv_task means send_task is going to stop"
            )
            await wait_task_result(self._send_task)

    async def _force_close_ws(self):
        with contextlib.suppress(BaseException):
            await self.websocket.close()

    async def change_language(self, language: LanguageCode) -> None:
        self.logger.debug(f"speech-to-text: {id(self)}-{self.connection_count} start change_language")
        self._raise_if_error_set()
        if self.language == language:
            self.logger.warning(f"speech-to-text: {id(self)}-{self.connection_count} passed if the language is the same")
            return
        self.language = language
        await self._reconnection()
        self._raise_if_error_set()
        self.logger.debug(f"speech-to-text: {id(self)}-{self.connection_count} create new connection successfully")

    async def _reconnection(self) -> None:
        reconnect_done = asyncio.Event()
        self._bg_command_queue.put_nowait(reconnect_done)
        await reconnect_done.wait()

    def _raise_if_error_set(self) -> None:
        if self._error_raised.is_set():
            raise self._last_exec

    async def _soft_close_bg_when_working(self):
        self.logger.debug(f"speech-to-text: {id(self)}-{self.connection_count}  wait until all data sent")
        send_queue = self._send_queue
        self._send_queue = asyncio.Queue()
        queue_done = asyncio.create_task(send_queue.join())
        await asyncio.wait([queue_done, self._send_task], return_when=asyncio.FIRST_COMPLETED)
        if queue_done.done():
            self.logger.debug(f"speech-to-text: {id(self)}-{self.connection_count}  all data sent")
            self._send_task.cancel()
        else:
            self.logger.debug(
                (
                    f"speech-to-text: {id(self)}-{self.connection_count} "
                    f"some error: {get_task_result(self._send_task)} raised during waiting."
                )
            )
            queue_done.cancel()

        try:
            await self.websocket.send(self._send_handler(StopCommand()))
            await asyncio.wait_for(self._recv_task, 10)
        except SeavoiceException:
            await asyncio.wait([self._recv_task])

    async def _authentication(self):
        try:
            await self.websocket.send(
                self._send_handler(
                    SpeechRecognitionAuthenticationCommand(
                        payload=SpeechRecognitionAuthenticationPayload(
                            token=self.token,
                            settings=SpeechRecognitionSetting(
                                language=self.language,
                                sample_rate=self.sample_rate,
                                itn=self.enable_itn,
                                punctuation=self.enable_punctuation,
                                contexts=self.contexts or {},
                                context_score=self.context_score,
                                stt_server_id=self.stt_server_id,
                            ),
                        )
                    )
                )
            )
        except UnExpectedClosedException as e:
            raise e
        except BaseException as e:
            raise AuthenticationFail(message=f"send auth command fails, error: {e}")

        try:
            event = self._recv_handler(await self.websocket.recv())
        except UnExpectedClosedException as e:
            raise e
        except BaseException as e:
            raise AuthenticationFail(message=f"receive and parse event fails, error: {e}")

        if not isinstance(event, InfoEvent) or event.payload.status != SpeechStatus.BEGIN:
            raise AuthenticationFail(message=f"receive unexpected event: {event}")

        self._recv_queue.put_nowait(event)

    async def recv(self) -> BaseEvent:
        recv = asyncio.create_task(self._recv_queue.get())
        error = asyncio.create_task(self._error_raised.wait())
        await asyncio.wait([recv, error], return_when=asyncio.FIRST_COMPLETED)

        if recv.done():
            error.cancel()
            return recv.result()

        recv.cancel()
        raise self._last_exec

    async def send(self, audio_data: bytes) -> None:
        self._raise_if_error_set()
        is_audio_done = asyncio.Event()
        self._send_queue.put_nowait(
            MultiCommands(
                commands=[
                    AudioDataCommand(payload=audio_data[i : i + self.chunk_size])
                    for i in range(0, len(audio_data), self.chunk_size)
                ],
                done=is_audio_done
            )
        )
        await is_audio_done.wait()

    async def finish(self) -> None:
        is_finish_done = asyncio.Event()
        self._send_queue.put_nowait(
            MultiCommands(
                commands=[StopCommand()],
                done=is_finish_done
            )
        )
        await is_finish_done.wait()

    async def stream(self) -> AsyncIterator[BaseEvent]:
        while True:
            try:
                yield (await self.recv())
            except ClosedException:
                return
            except BaseException as e:
                raise e

    async def _send_from_queue(self) -> None:
        send_queue = self._send_queue
        while True:
            data = await send_queue.get()
            assert isinstance(data, MultiCommands)
            try:
                for command in data.commands:
                    await self.websocket.send(self._send_handler(command))
                    await asyncio.sleep(self.send_chunk_interval)
            finally:
                send_queue.task_done()
                data.done.set()

    async def _recv_to_queue(self) -> None:
        while True:
            self._recv_queue.put_nowait(self._recv_handler(await self.websocket.recv()))

    def _recv_handler(self, data: Union[str, bytes]) -> BaseEvent:
        event = raw_data_to_event(**json.loads(data))
        if isinstance(event, RecognizingEvent) or isinstance(event, RecognizedEvent):
            self._recv_segment_id = event.payload.segment_id
            event.payload.segment_id += self._segment_id_offset
            event.payload.voice_start_time += self._voice_start_offset
            for word_aliment in event.payload.word_alignments:
                word_aliment.start += self._voice_start_offset
        return event

    def _send_handler(self, data: BaseCommand):
        if isinstance(data, AudioDataCommand):
            self._sent_bytes += len(data.payload)
        return json.dumps(data.to_dict())
