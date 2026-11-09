import os
from dotenv import load_dotenv
from gnani.tts import GnaniTTSClient, AudioConfig

load_dotenv()

api_key = os.getenv("GNANI_API_KEY")

if not api_key:
    raise ValueError("API key missing in .env")

print("Connecting to Gnani AI...")

client = GnaniTTSClient(api_key=api_key)

audio = client.synthesize(
    "Welcome to SpeakSmart India. Let's practice interviews.",
    voice="Nalini",
    model="timbre-v2.5",
    language="en-IN",
    audio_config=AudioConfig(
        container="wav",
        sample_rate=48000
    )
)

with open("welcome.wav", "wb") as f:
    f.write(audio)

print("Success! Gnani AI generated your audio.")