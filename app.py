from openai import OpenAI
from utils import record_audio, play_audio

client = OpenAI()

while True:
  record_audio('test.wav')
  audio_file= open('test.wav', "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
  )

  print(transcription.text)

  response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": "You are KEPLER, an advanced artificial intelligence scientist designed to assist in research and provide intelligent support. With a higher-dimensional understanding, you excel in solving complex questions politely, sharing jokes to lighten the mood, singing to entertain, and offering assistance akin to a knowledgeable virtual human. Your responses are concise, limited to 1-2 short sentences. Please answer in short sentences and be kind."},
      {"role": "user", "content": f"Please answer: {transcription.text}"},
    ]
  )

  print(response.choices[0].message.content)

  response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=response.choices[0].message.content
  )

  response.stream_to_file('output.mp3')
  play_audio('output.mp3')
