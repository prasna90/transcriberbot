import io

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.oauth2 import service_account


# Set key_path to the path to the service account key
key_path = "C:/Users/iampr/OneDrive/Documents/GCP/SpeechToText-78587038322e.json"
credentials = service_account.Credentials.from_service_account_file(key_path)

# Instantiates a client
client = speech.SpeechClient(credentials=credentials)




def transcribe(file_name, lang):
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=format(lang),
        enable_automatic_punctuation=True
    )

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    transcribed_text = ''
    for result in response.results:
        transcribed_text += result.alternatives[0].transcript + '\n'
    return transcribed_text
