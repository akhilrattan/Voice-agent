from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # loads .env file

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MODEL="openai/gpt-4o-mini"

messages = [
    {"role": "system", "content": """
You are Aria, a sharp voice assistant.
Keep every reply under 2 sentences.
Never use bullet points or markdown — you are speaking out loud.
Speak naturally and concisely.
"""}
]

def get_reply(user_text):
    """Get LLM reply. Returns complete reply string."""
    messages.append({"role": "user", "content": user_text})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply

    except Exception as e:
        messages.pop()
        print(f"LLM error: {e}")
        return "Sorry, I ran into an issue. Please try again."

def get_reply_streaming(user_text):
    """
    Stream LLM reply sentence by sentence.
    Yields each sentence as soon as it's complete.
    Lets TTS start speaking before full reply is done.
    """
    messages.append({"role": "user", "content": user_text})
    full_reply = ""
    current_sentence = ""

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=150,
            stream=True   # this is the key change
        )

        for chunk in stream:
            word = chunk.choices[0].delta.content
            if word is None:
                continue

            current_sentence += word
            full_reply += word

            # yield a sentence when we hit a natural pause
            if any(current_sentence.endswith(p) for p in [".", "!", "?"]):
                yield current_sentence.strip()
                current_sentence = ""

        # yield anything remaining
        if current_sentence.strip():
            yield current_sentence.strip()

        messages.append({"role": "assistant", "content": full_reply})

    except Exception as e:
        messages.pop()
        print(f"LLM error: {e}")
        yield "Sorry, I ran into an issue. Please try again."