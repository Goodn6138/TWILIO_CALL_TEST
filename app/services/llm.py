from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# simple in-memory conversation (upgrade later if needed)
conversation = [
    {
        "role": "system",
        "content": "You are a helpful voice assistant. Keep responses short, clear, and conversational."
    }
]

def generate_reply(text):
    """
    Generate AI response using Groq LLM
    """
    try:
        conversation.append({"role": "user", "content": text})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation
        )

        reply = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": reply})

        return reply

    except Exception as e:
        print("LLM Error:", e)
        return "Sorry, something went wrong."
