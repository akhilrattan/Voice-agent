import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

SAMPLE_RATE = 16000
DURATION = 5
TEMP_FILE = "temp_recording.wav"

# Load once when this module is imported — not on every call
model = whisper.load_model("base")
print("Whisper model loaded.")

def record_audio(duration=DURATION):
    """Record audio from mic and save to a temp file."""
    print("Recording — speak now!")
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16
    )
    sd.wait()
    write(TEMP_FILE, SAMPLE_RATE, audio)
    print("Recording done.")

def transcribe():
    """Transcribe the last recorded audio file. Returns text string."""
    result = model.transcribe(TEMP_FILE)
    return result["text"].strip()

def listen():
    """Record and transcribe in one step. Returns text string."""
    record_audio()
    return transcribe()