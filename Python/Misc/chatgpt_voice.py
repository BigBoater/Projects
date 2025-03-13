from pathlib import Path
from openai import OpenAI
client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input="This is what my voice sounds like 10 days into ChatGPT!"
)

response.stream_to_file(speech_file_path)
