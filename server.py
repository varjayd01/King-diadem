from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app import decision_engine, detect_emotion
import json, os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# memory
user_profile = {}
group_chat = []

# ---------------- AI CHAT ----------------
@app.post("/ask")
async def ask(req: Request):
    data = await req.json()
    q = data.get("question", "")

    ans = decision_engine(q, user_profile)

    # save log
    os.makedirs("data", exist_ok=True)
    path = "data/log.json"

    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)

    with open(path, "r") as f:
        logs = json.load(f)

    logs.append({"q": q, "a": ans})

    with open(path, "w") as f:
        json.dump(logs, f)

    return JSONResponse({"answer": ans})


# ---------------- PERSONA ----------------
@app.post("/save_profile")
async def save(req: Request):
    data = await req.json()
    user_profile.update(data)
    return {"status": "ok"}


# ---------------- GROUP CHAT ----------------
@app.post("/group_send")
async def group_send(req: Request):
    data = await req.json()
    msg = data.get("msg", "")

    emo = detect_emotion(msg)

    group_chat.append({"msg": msg, "emotion": emo})

    # auto AI help
    if emo == "crisis":
        ai = decision_engine(msg, {})
        group_chat.append({"msg": "🤖 " + ai, "emotion": "ai"})

    return {"status": "ok"}


@app.get("/group_get")
async def group_get():
    return {"messages": group_chat[-20:]}


# ---------------- DASHBOARD ----------------
@app.get("/dashboard")
async def dash():
    try:
        with open("data/log.json") as f:
            logs = json.load(f)
    except:
        logs = []

    return {
        "total": len(logs),
        "recent": logs[-5:]
    }


# ---------------- HOME ----------------
@app.get("/")
async def root():
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())
