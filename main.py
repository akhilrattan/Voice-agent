import time
from voice.input import listen
from llm.aria import get_reply_streaming
from txt_to_speech.tts import speak

print("\nAria is ready. Press Enter to speak, Ctrl+C to quit.\n")

while True:
    try:
        input("[ Press Enter to speak ]")

        # Step 1: Record and transcribe
        t0 = time.time()
        user_text = listen()
        t1 = time.time()

        if not user_text:
            print("Didn't catch that. Try again.\n")
            continue

        print(f"You said: {user_text}")
        print(f"[Whisper: {t1-t0:.2f}s]")

        # Step 2+3: Stream LLM reply and speak each sentence immediately
        print("Aria: ", end="", flush=True)
        t2 = time.time()

        for sentence in get_reply_streaming(user_text):
            print(sentence, end=" ", flush=True)
            speak(sentence)  # speak each sentence as it arrives

        t3 = time.time()
        print(f"\n[LLM+TTS total: {t3-t2:.2f}s]\n")

    except KeyboardInterrupt:
        print("\nAria: Goodbye!")
        break
    except Exception as e:
        print(f"Error: {e}\n")
