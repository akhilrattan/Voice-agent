from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # loads .env file

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MODEL="openai/gpt-4o-mini"

# Conversation history lives here — persists for the whole session
messages = [
    {"role": "system", "content": """
You are Aria, a sharp voice assistant.
Keep every reply under 2 sentences.
Never use bullet points or markdown — you are speaking out loud.
Speak naturally and concisely.
"""}
]

def get_reply(user_text):
    """Send user text to LLM, return assistant reply string."""
    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply

def get_history():
    """Return conversation history — useful for debugging."""
    return messages