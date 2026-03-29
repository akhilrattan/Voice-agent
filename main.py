from voice.input import listen
from llm.aria import get_reply
from txt_to_speech.tts import speak          # ← new

print("\nAria is ready. Press Enter to speak, Ctrl+C to quit.\n")

while True:
    try:
        input("[ Press Enter to speak ]")

        # Step 1: Record and transcribe
        user_text = listen()

        if not user_text:
            print("Didn't catch that. Try again.\n")
            continue

        print(f"You said: {user_text}")

        # Step 2: Get LLM reply
        print("Aria is thinking...")
        reply = get_reply(user_text)

        print(f"Aria: {reply}")

        # Step 3: Speak the reply        ← new
        speak(reply)

    except KeyboardInterrupt:
        print("\nAria: Goodbye!")
        break
    except Exception as e:
        print(f"Error: {e}\n")