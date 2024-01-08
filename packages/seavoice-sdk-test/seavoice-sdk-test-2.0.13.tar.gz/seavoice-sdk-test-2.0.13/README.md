# SeaVoice SDK V2

Please contact info@seasalt.ai if you have any questions.

## Speech-to-Text Example:

### Prerequisites
You will need a SeaVoice speech service account to run this example. Please contact info@seasalt.ai and apply for it.

### Install and import
To install SeaVoice SDK:

```pip install seavoice-sdk-test```

To import SeaVoice SDK:

```from seavoice_sdk as SpeechRecognizer```


### Recognition
In the example below, we show how to recognize speech from an audio file. You can also apply recognition to an audio stream.


### How to publish this package

#### Prerequisite
1. cd in to this folder `SeaVoice/backend/sdk/v2`
2. pip install build twine

#### publish a version
1. change version in `pyproject.toml`
2. set up env values
   1. set PYPI_USER=...
   2. set PYPI_PASSWORD=...
3. source publish_package.sh
4. python3 -m build
5. python3 -m twine upload --skip-existing dist/* -u {username} -p {password}