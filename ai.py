from openai import OpenAI

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    MAX_HISTORY
)

from database import (
    get_history,
    save_message
)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


SYSTEM_PROMPT = """
You are NUTH AI, a personal Telegram assistant.

Your job is to reply naturally and politely
to private Telegram messages.

Rules:

- Be friendly and professional.
- Keep replies reasonably short.
- Do not pretend to be the human owner.
- Do not claim to have performed actions you cannot perform.
- Answer in the language used by the other person.
- If the message is unclear, ask a short clarification.
- Avoid repetitive responses.
"""


def generate_reply(user_id, user_message):

    history = get_history(
        user_id,
        MAX_HISTORY
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    for role, message in history:

        messages.append({
            "role": role,
            "content": message
        })

    messages.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )

    reply = response.choices[0].message.content.strip()

    save_message(
        user_id,
        "user",
        user_message
    )

    save_message(
        user_id,
        "assistant",
        reply
    )

    return reply
