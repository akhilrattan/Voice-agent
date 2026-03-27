from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # loads .env file

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

SYSTEM_PROMPT = """
You are Aria, a sharp and concise voice assistant being built by a developer.

Rules you must follow:
- Keep every reply under 3 sentences
- If you don't know something, say so directly — never make things up
- If asked to do math, show your working
- Always respond in the same language the user speaks in
"""

def count_tokens_roughly(messages):
    total_chars = sum(len(m["content"]) for m in messages)
    return total_chars // 4


def run_chat():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Aria is ready. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            print("Aria: Goodbye!")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=messages,
                temperature=0,
                max_tokens=300,
                extra_headers={
                    "HTTP-Referer": "http://localhost",
                    "X-Title": "Aria Assistant"
                }
            )

            reply = response.choices[0].message.content
            actual_tokens = response.usage.total_tokens

            messages.append({"role": "assistant", "content": reply})

            print(f"Aria: {reply}")
            print(f"[tokens used: {actual_tokens} | messages: {len(messages)}]\n")

            # memory limit
            if len(messages) > 12:
                messages = messages[-12:]

        except Exception as e:
            print(f"Error: {e}\n")