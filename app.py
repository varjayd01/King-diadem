from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# serve UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")


# ===== API KEY =====
OPENAI_API_KEY = os.getenv("CHATGPT_API_KEY")


# ===== INPUT MODEL =====
class ChatInput(BaseModel):
    message: str


# ===== CALL OPENAI =====
def call_openai(message):

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    res = requests.post(url, headers=headers, json=data)

    try:
        return res.json()["choices"][0]["message"]["content"]
    except:
        return str(res.text)


# ===== CHAT ENDPOINT =====
@app.post("/chat")
def chat(data: ChatInput):

    if not data.message:
        return {"reply": "..."}

    reply = call_openai(data.message)

    return {"reply": reply}
