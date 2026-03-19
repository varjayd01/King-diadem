from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app import decision_engine, detect_emotion

import json, os, uuid

app = FastAPI()

# ------------------- CORS (สำคัญมาก) -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- STATIC -------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# ------------------- MEMORY -------------------
user_profile = {}
group_chat = []

# chat sessions (เหมือน ChatGPT)
chat_sessions = {}  # {chat_id: [ {q,a} ]}

# ------------------- UTILS -------------------
def load_logs(chat_id):
    path = f"data/{chat_id}.json"
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_logs(chat_id, logs):
    os.makedirs("data", exist_ok=True)
    path = f"data/{chat_id}.json"
    with open(path, "w") as f:
        json.dump(logs, f)

# ------------------- NEW CHAT -------------------
@app.post("/new_chat")
async def new_chat():
    chat_id = str(uuid.uuid4())
    chat_sessions[chat_id] = []
    return {"chat_id": chat_id}

# ------------------- AI CHAT -------------------
@app.post("/ask")
async def ask(req: Request):
    try:
        data = await req.json()
        q = data.get("question", "")
        chat_id = data.get("chat_id")

        if not chat_id:
            return JSONResponse({"error": "chat_id required"}, status_code=400)

        ans = decision_engine(q, user_profile)

        logs = load_logs(chat_id)
        logs.append({"q": q, "a": ans})
        save_logs(chat_id, logs)

        return JSONResponse({
            "answer": ans,
            "chat_id": chat_id,
            "length": len(logs)
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ------------------- GET CHAT HISTORY -------------------
@app.get("/chat/{chat_id}")
async def get_chat(chat_id: str):
    logs = load_logs(chat_id)
    return {"messages": logs}

# ------------------- PERSONA -------------------
@app.post("/save_profile")
async def save(req: Request):
    data = await req.json()
    user_profile.update(data)
    return {"status": "ok", "profile": user_profile}

# ------------------- GROUP CHAT -------------------
@app.post("/group_send")
async def group_send(req: Request):
    data = await req.json()
    msg = data.get("msg", "")

    emo = detect_emotion(msg)

    group_chat.append({
        "msg": msg,
        "emotion": emo,
        "type": "user"
    })

    # auto AI assist
    if emo == "crisis":
        ai = decision_engine(msg, {})
        group_chat.append({
            "msg": ai,
            "emotion": "ai",
            "type": "ai"
        })

    return {"status": "ok"}

@app.get("/group_get")
async def group_get():
    return {"messages": group_chat[-50:]}

# ------------------- DASHBOARD -------------------
@app.get("/dashboard")
async def dash():
    try:
        files = os.listdir("data")
        total = len(files)
    except:
        total = 0

    return {
        "total_chats": total,
        "system": "KING DIADEM ACTIVE"
    }

# ------------------- HOME -------------------
@app.get("/")
async def root():
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())
