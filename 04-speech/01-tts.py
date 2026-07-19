# sudo apt-get install libasound2t64

import azure.cognitiveservices.speech as speechsdk
import os
from azure.identity import AzureCliCredential


def create_speech_config() -> None:
    global speech_config
    resource_id = os.environ["AZURE_RESOURCE_ID"]
    credential = AzureCliCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    speech_config = speechsdk.SpeechConfig(endpoint=os.environ["AZURE_SPEECH_ENDPOINT"])
    speech_config.authorization_token = f"aad#{resource_id}#{token.token}"
    speech_config.speech_synthesis_voice_name = os.environ["SPEECH_VOICE_NAME"]


def speech(text: str, output_filename: str) -> None:
    audio_config = speechsdk.audio.AudioConfig(filename=output_filename)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config, audio_config)
    speech_synthesizer.speak_text_async(text).get()


create_speech_config()
speech(
    "今日もお疲れ様でした! 明日も頑張ろう。高レベルラッパーを使用すると便利。",
    "sample.wav",
)
