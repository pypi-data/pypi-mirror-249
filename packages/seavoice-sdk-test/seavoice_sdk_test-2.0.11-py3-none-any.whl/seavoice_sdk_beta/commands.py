# -*- coding: utf-8 -*-

"""
The commands of seavoice-sdk
"""
import base64
from abc import ABC
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, ClassVar, Optional


class SpeechCommand(str, Enum):
    STOP = "stop"
    AUTHENTICATION = "authentication"
    AUDIO_DATA = "audio_data"
    SYNTHESIS = "synthesis"


class Voice(str, Enum):
    TONGTONG = "Tongtong"
    VIVIAN = "Vivian"
    MIKE = "Mike"
    MOXIE = "Moxie"
    LISSA = "Lissa"
    TOM = "Tom"
    ROBERT = "Robert"
    DAVID = "David"
    ANNE = "Anne"
    REESE = "Reese"


class LanguageCode(str, Enum):
    EN_US = "en-US"
    EN_GB = "en-GB"
    ZH_TW = "zh-TW"


VOICE_LANGUAGES_MAPPING = {
    Voice.TONGTONG: [LanguageCode.ZH_TW],
    Voice.VIVIAN: [LanguageCode.ZH_TW],
    Voice.MIKE: [LanguageCode.EN_US],
    Voice.MOXIE: [LanguageCode.EN_US],
    Voice.LISSA: [LanguageCode.EN_US],
    Voice.TOM: [LanguageCode.EN_US],
    Voice.ROBERT: [LanguageCode.EN_US],
    Voice.DAVID: [LanguageCode.EN_GB],
    Voice.ANNE: [LanguageCode.EN_US],
    Voice.REESE: [LanguageCode.EN_US],
}


@dataclass
class AbstractDataclass(ABC):
    def __new__(cls, *args, **kwargs):
        if cls == AbstractDataclass or cls.__bases__[0] == AbstractDataclass:
            raise TypeError("Cannot instantiate abstract class.")
        return super().__new__(cls)


@dataclass
class BaseCommand(AbstractDataclass):
    command: ClassVar[SpeechCommand]
    payload: Any

    def to_dict(self) -> dict:
        return {"command": self.command, "payload": asdict(self.payload)}


@dataclass
class StopCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.STOP
    payload: Any = None

    def to_dict(self) -> dict:
        return {"command": self.command}


@dataclass
class BaseAuthenticationPayload(AbstractDataclass):
    token: str
    settings: Any


@dataclass
class SpeechRecognitionSetting:
    language: str
    sample_rate: int
    itn: bool
    punctuation: bool
    contexts: dict
    context_score: float
    stt_server_id: Optional[str]


@dataclass
class SpeechRecognitionAuthenticationPayload(BaseAuthenticationPayload):
    token: str
    settings: SpeechRecognitionSetting


@dataclass
class SpeechRecognitionAuthenticationCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.AUTHENTICATION
    payload: SpeechRecognitionAuthenticationPayload


@dataclass
class SpeechSynthesisSetting:
    language: LanguageCode
    voice: Voice
    tts_server_id: Optional[str]


@dataclass
class SpeechSynthesisAuthenticationPayload(BaseAuthenticationPayload):
    token: str
    settings: SpeechSynthesisSetting


@dataclass
class SpeechSynthesisAuthenticationCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.AUTHENTICATION
    payload: SpeechSynthesisAuthenticationPayload


@dataclass
class AudioDataCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.AUDIO_DATA
    payload: bytes

    def to_dict(self) -> dict:
        return {
            "command": self.command,
            "payload": base64.b64encode(self.payload).decode(),
        }


@dataclass
class SynthesisSettings:
    pitch: float
    speed: float
    volume: float
    rules: str
    sample_rate: int


@dataclass
class SynthesisData:
    text: str
    ssml: bool


@dataclass
class SynthesisPayload:
    settings: SynthesisSettings
    data: SynthesisData


@dataclass
class SynthesisCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.SYNTHESIS
    payload: SynthesisPayload
