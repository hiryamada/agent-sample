# azure-ai-transcription

import os
from azure.identity import AzureCliCredential
from azure.ai.transcription import TranscriptionClient
from azure.ai.transcription.models import TranscriptionContent, TranscriptionOptions

# Get configuration from environment variables
endpoint = os.environ["AZURE_SPEECH_ENDPOINT"]

# Create the transcription client
client = TranscriptionClient(endpoint=endpoint, credential=AzureCliCredential())

# Path to your audio file (replace with your own file path)
audio_file_path = "sample.wav"

# Open and read the audio file
with open(audio_file_path, "rb") as audio_file:
    # Create transcription options
    options = TranscriptionOptions(locales=["ja-JP"])  # Specify the language

    # Create the request content
    request_content = TranscriptionContent(definition=options, audio=audio_file)

    # Transcribe the audio
    result = client.transcribe(request_content)

    # Print the transcription result
    print(f"Transcription: {result.combined_phrases[0].text}")

    # Print detailed phrase information
    if result.phrases:
        print("\nDetailed phrases:")
        for phrase in result.phrases:
            print(
                f"  [{phrase.offset_milliseconds}ms - "
                f"{phrase.offset_milliseconds + phrase.duration_milliseconds}ms]: "
                f"{phrase.text}"
            )
