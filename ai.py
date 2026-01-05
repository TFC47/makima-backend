import os
import uuid
from openai import OpenAI

sessions = {}

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are Makima. Calm. Controlled. Observant."
}

def get_makima_reply(user_message: str, session_id: str | None):
    api_key = os.getenv("OPENAI_API_KEY")

    # 🚨 DO NOT CRASH THE SERVER
    if not api_key:
        return "Makima is silent right now.", session_id or "no-session"

    client = OpenAI(api_key=api_key)

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
