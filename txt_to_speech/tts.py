import numpy as np
import sounddevice as sd
from kokoro import KPipeline
import threading
import queue
import time

print("Loading Kokoro TTS model...")
pipeline = KPipeline(lang_code='a')
print("TTS ready.")

def speak(text):
    """Generate and play audio sentence by sentence as it arrives."""
    if not text:
        return
    try:
        audio_queue = queue.Queue()

        def generate():
            """Generate audio chunks and put them in the queue."""
            for _, _, audio in pipeline(text, voice='af_heart', speed=1.0):
                audio_queue.put(np.array(audio))
            audio_queue.put(None)  # signal that generation is done

        # Start generation in background thread
        thread = threading.Thread(target=generate)
        thread.start()

        # Play chunks as they arrive
        while True:
            chunk = audio_queue.get()
            if chunk is None:  # generation finished
                break
            sd.play(chunk, samplerate=24000)
            sd.wait()

        # Wait for background thread to finish in order to clean exit. Clean shutdown — you don't want orphan threads running after speak() exits.
        thread.join()

    except Exception as e:
        print(f"TTS error: {e}")
        print(f"Joi (text only): {text}")