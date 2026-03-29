import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import whisper

SAMPLE_RATE = 16000
DURATION = 5
TEMP_FILE = "temp_recording.wav"
SILENCE_THRESHOLD = 500  # audio energy below this = probably silence

print("Loading Whisper model...")
model = whisper.load_model("base")
print("Voice module ready.")

def record_audio(duration=DURATION):
    """Record audio from mic and save to temp file."""
    print("Recording — speak now!")
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16
    )
    sd.wait()
    write(TEMP_FILE, SAMPLE_RATE, audio)
    return audio

def is_silent(audio):
    """Check if recording is basically silence — no point transcribing."""
    energy = np.abs(audio).mean()
    return energy < SILENCE_THRESHOLD

def transcribe():
    """Transcribe audio file. Returns text or empty string."""
    result = model.transcribe(TEMP_FILE)
    return result["text"].strip()

def listen():
    """
    Record and transcribe in one step.
    Returns transcribed text, or empty string if silent/failed.
    """
    audio = record_audio()

    # Guard 1 — silence check
    if is_silent(audio):
        print("No speech detected.")
        return ""

    # Guard 2 — transcribe with error handling
    try:
        text = transcribe()
    except Exception as e:
        print(f"Transcription failed: {e}")
        return ""

    # Guard 3 — whisper sometimes returns filler with no real content
    junk_phrases = ["thank you", "thanks for watching", "bye", "you"]
    if len(text) < 3 or text.lower().strip() in junk_phrases:
        print("Transcript too short or junk — try again.")
        return ""

    return text