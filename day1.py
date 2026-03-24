from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)
messages = [
    {"role": "system", "content": "You are a helpful AI assistant."}
]

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("AI: Goodbye Akhil 👋")
        break
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content
    print("AI:", reply)

    messages.append({"role": "assistant", "content": reply})
