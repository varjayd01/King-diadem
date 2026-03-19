from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app import decision_engine, detect_emotion

import json, os, uuid

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- STATIC ----------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- MEMORY ----------------
user_profiles = {}
chat_sessions = {}

# ---------------- UTILS ----------------
def path(chat_id):
    return f"data/{chat_id}.json"

def load(chat_id):
    if not os.path.exists(path(chat_id)):
        return []
    with open(path(chat_id), "r") as f:
        return json.load(f)

def save(chat_id, logs):
    os.makedirs("data", exist_ok=True)
    with open(path(chat_id), "w") as f:
        json.dump(logs, f)

# ---------------- NEW CHAT ----------------
@app.post("/new_chat")
async def new_chat():
    chat_id = str(uuid.uuid4())
    chat_sessions[chat_id] = []
    return {"chat_id": chat_id}

# ---------------- CHAT ----------------
@app.post("/ask")
async def ask(req: Request):
    data = await req.json()

    q = data.get("question", "")
    chat_id = data.get("chat_id")

    if not chat_id:
        return JSONResponse({"error": "no chat_id"}, status_code=400)

    ans = decision_engine(q, user_profiles.get(chat_id, {}))

    logs = load(chat_id)
    logs.append({"q": q, "a": ans})
    save(chat_id, logs)

    return {"answer": ans}

# ---------------- HISTORY ----------------
@app.get("/chat/{chat_id}")
async def history(chat_id: str):
    return {"messages": load(chat_id)}

# ---------------- HOME ----------------
@app.get("/")
async def root():
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())
