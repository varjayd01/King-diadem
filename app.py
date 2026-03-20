from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uuid, json, os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def path(chat_id):
    return f"data/{chat_id}.json"

def load(chat_id):
    if not os.path.exists(path(chat_id)):
        return []
    return json.load(open(path(chat_id)))

def save(chat_id, data):
    os.makedirs("data", exist_ok=True)
    json.dump(data, open(path(chat_id), "w"))

# ---------------- UI ----------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ---------------- CHAT ----------------
@app.post("/new_chat")
async def new_chat():
    return {"chat_id": str(uuid.uuid4())}

@app.post("/ask")
async def ask(req: Request):
    data = await req.json()
    chat_id = data["chat_id"]
    q = data["question"]

    ans = f"ตอบ: {q}"  # test ก่อน

    logs = load(chat_id)
    logs.append({"q": q, "a": ans})
    save(chat_id, logs)

    return {"answer": ans}

@app.get("/chat/{chat_id}")
async def chat(chat_id: str):
    return {"messages": load(chat_id)}
