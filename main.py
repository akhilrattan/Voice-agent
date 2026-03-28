from voice.input import listen
from llm.aria import get_reply

print("\nAria is ready. Press Enter to speak, Ctrl+C to quit.\n")

while True:
    try:
        input("[ Press Enter to speak ]")

        # Step 1: voice.py handles recording + transcription
        user_text = listen()

        if not user_text:
            print("Didn't catch that. Try again.\n")
            continue

        print(f"You said: {user_text}")

        # Step 2: llm.py handles the reply
        print("Aria is thinking...")
        reply = get_reply(user_text)

        print(f"\nAria: {reply}\n")

    except KeyboardInterrupt:
        print("\nAria: Goodbye!")
        break
    except Exception as e:
        print(f"Error: {e}\n")