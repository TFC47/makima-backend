from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai import get_makima_reply

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

@app.post("/chat")
def chat(req: ChatRequest):
    reply, session_id = get_makima_reply(req.message, req.session_id)
    return {
        "reply": reply,
        "session_id": session_id
    }
