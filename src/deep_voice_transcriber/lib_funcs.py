#!/usr/bin/python3

from openai import OpenAI

def deep_transcript(  mp3_file_path,
                      base_url="https://api.deepinfra.com/v1/openai",
                      api_key="",
                      model="openai/whisper-large-v3"
                      ):

    client = OpenAI(
        api_key = api_key,
        base_url = base_url,
    )

    audio_file = open(mp3_file_path, "rb")
    transcript = client.audio.transcriptions.create(
      model=model,
      file=audio_file
    )
    
    return transcript.text
