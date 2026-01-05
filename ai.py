import uuid
from openai import OpenAI

client = OpenAI()

sessions = {}

SYSTEM_PROMPT = {
    "role": "system",
    "content": """You are an AI assistant modeled after Makima..."""
}

def get_makima_reply(user_message: str, session_id: str | None):
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = [SYSTEM_PROMPT]

    sessions[session_id].append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=sessions[session_id],
        temperature=0.7
    )

    reply = response.choices[0].message.content

    sessions[session_id].append({
        "role": "assistant",
        "content": reply
    })

    return reply, session_id
