import numpy as np
import sounddevice as sd
from kokoro import KPipeline

# Load once at startup
print("Loading Kokoro TTS model...")
pipeline = KPipeline(lang_code='a')  # 'a' = American English
print("TTS ready.")

def speak(text):
    """Convert text to speech using Kokoro and play it."""
    if not text:
        return
    try:
        generator = pipeline(
            text,
            voice='af_heart',  # clear, natural female voice
            speed=1.0
        )

        for _, _, audio in generator:
            audio_array = np.array(audio)
            sd.play(audio_array, samplerate=24000)
            sd.wait()

    except Exception as e:
        print(f"TTS error: {e}")
        print(f"Aria (text only): {text}")