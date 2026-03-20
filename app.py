import os, json, uuid, time
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from google import genai
from google.genai import types

# =====================
# CONFIG
# =====================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "chats"
DATA_DIR.mkdir(parents=True, exist_ok=True)

USE_AI = True
MODEL_NAME = "gemini-1.5-flash"

client = None
if os.getenv("GEMINI_API_KEY"):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
else:
    USE_AI = False

# =====================
# APP
# =====================
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# =====================
# UTILS
# =====================
def now_iso():
    return datetime.now().isoformat()

def chat_path(cid):
    return DATA_DIR / f"{cid}.json"

def load_chat(cid):
    p = chat_path(cid)
    if not p.exists():
        return {"id": cid, "title": "New Chat", "messages": []}
    return json.loads(p.read_text())

def save_chat(chat):
    chat["updated_at"] = now_iso()
    chat_path(chat["id"]).write_text(json.dumps(chat, ensure_ascii=False, indent=2))

def list_chats():
    items = []
    for f in DATA_DIR.glob("*.json"):
        try:
            c = json.loads(f.read_text())
            items.append({
                "id": c["id"],
                "title": c["title"],
                "updated_at": c.get("updated_at", "")
            })
        except:
            pass
    return sorted(items, key=lambda x: x["updated_at"], reverse=True)

# =====================
# INTENT
# =====================
def detect_intent(text):
    t = text.lower()

    if len(t.split()) > 20:
        return "DEEP"

    if any(x in t for x in ["ไม่มีทางเลือก","จน","ไม่ไหว"]):
        return "SURVIVAL"

    if any(x in t for x in ["ควร","เลือก"]):
        return "DECISION"

    return "GENERAL"

# =====================
# CONTEXT
# =====================
def build_context(messages, limit=20):
    return "\n".join([f"{m['role']}: {m['content']}" for m in messages[-limit:]])

# =====================
# SYSTEM FALLBACK
# =====================
def decision_engine(intent, q):
    if intent == "SURVIVAL":
        return "เริ่มจากลดความเสี่ยงก่อน แล้วค่อยหาทางเพิ่มทางเลือก"
    if intent == "DECISION":
        return "แยกทางเลือก → ดู downside → เลือกทางที่พังยากสุด"
    return None

def fallback_engine(intent, q):
    if intent == "SURVIVAL":
        return "รักษาสิ่งที่ยังไม่พังก่อน"
    if intent == "DECISION":
        return "เลือกทางที่เสียหายน้อยที่สุดก่อน"
    return "⚠️ AI ไม่พร้อม แต่ระบบยังทำงาน"

# =====================
# GEMINI
# =====================
def gemini_answer(q, context, intent):
    if not USE_AI or client is None:
        raise RuntimeError("AI OFF")

    system_instruction = """
You are KING DIadem AI.

Style:
- Smart, calm
- 5-10 lines
- No fluff
"""

    prompt = f"""
Context:
{context}

User:
{q}
"""

    res = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.6
        )
    )

    return getattr(res, "text", "").strip()

# =====================
# ROUTES
# =====================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/new_chat")
def new_chat():
    cid = str(uuid.uuid4())
    chat = {"id": cid, "title": "New Chat", "messages": []}
    save_chat(chat)
    return {"chat_id": cid}

@app.get("/chats")
def chats():
    return {"chats": list_chats()}

@app.post("/ask_stream")
async def ask_stream(req: Request):
    data = await req.json()
    cid = data["chat_id"]
    q = data["question"]

    chat = load_chat(cid)

    chat["messages"].append({
        "role": "user",
        "content": q,
        "timestamp": now_iso()
    })

    context = build_context(chat["messages"])
    intent = detect_intent(q)

    try:
        answer = gemini_answer(q, context, intent)
    except:
        answer = decision_engine(intent, q) or fallback_engine(intent, q)

    chat["messages"].append({
        "role": "assistant",
        "content": answer,
        "timestamp": now_iso()
    })

    save_chat(chat)

    def stream():
        for w in answer.split():
            yield w + " "
            time.sleep(0.02)

    return StreamingResponse(stream(), media_type="text/plain")
