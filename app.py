from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from google import genai
from google.genai import types

from pathlib import Path
from datetime import datetime
import os
import json
import uuid
import re

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

USE_AI = False
client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        USE_AI = True
    except Exception as e:
        print("Gemini init error:", e)
        USE_AI = False


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def safe_title(text: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9ก-๙]+", text)
    title = " ".join(tokens[:5]).strip()
    return title[:48] if title else "New Chat"


def chat_path(chat_id: str) -> Path:
    return DATA_DIR / f"{chat_id}.json"


def default_chat(chat_id: str) -> dict:
    ts = now_iso()
    return {
        "id": chat_id,
        "title": "New Chat",
        "created_at": ts,
        "updated_at": ts,
        "messages": []
    }


def load_chat(chat_id: str) -> dict:
    path = chat_path(chat_id)
    if not path.exists():
        return default_chat(chat_id)

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if "messages" not in data:
        data["messages"] = []
    if "title" not in data:
        data["title"] = "New Chat"
    if "created_at" not in data:
        data["created_at"] = now_iso()
    if "updated_at" not in data:
        data["updated_at"] = now_iso()

    return data


def save_chat(chat: dict) -> None:
    chat["updated_at"] = now_iso()
    path = chat_path(chat["id"])
    with path.open("w", encoding="utf-8") as f:
        json.dump(chat, f, ensure_ascii=False, indent=2)


def list_chats() -> list[dict]:
    items = []
    for path in DATA_DIR.glob("*.json"):
        try:
            chat = load_chat(path.stem)
            last_msg = chat["messages"][-1]["content"] if chat["messages"] else ""
            preview = last_msg[:90]
            items.append({
                "id": chat["id"],
                "title": chat["title"],
                "updated_at": chat["updated_at"],
                "count": len(chat["messages"]),
                "preview": preview,
            })
        except Exception:
            continue

    items.sort(key=lambda x: x["updated_at"], reverse=True)
    return items


def detect_intent(text: str) -> str:
    q = text.lower()

    if any(x in q for x in ["ไม่มีทางเลือก", "หมดทาง", "จน", "ไม่ไหว", "พัง"]):
        return "SURVIVAL"

    if any(x in q for x in ["ควร", "ทำยังไง", "แนะนำ", "เลือกอะไร"]):
        return "DECISION"

    if any(x in q for x in ["คืออะไร", "อธิบาย", "ทำไม"]):
        return "LEARN"

    return "GENERAL"


def decision_engine(intent: str, question: str) -> str | None:
    if intent == "SURVIVAL":
        return "เริ่มจากลดความเสี่ยงก่อน ค่อยหาทางเลือกใหม่ทีละก้าว"

    if intent == "DECISION":
        return "แยกทางเลือก ประเมิน downside แล้วเลือกทางที่รอดก่อน"

    if intent == "LEARN":
        return "อธิบายให้สั้น ชัด และใช้ได้จริง"

    if len(question.strip()) <= 2:
        return "ลองพิมพ์เพิ่มอีกนิดนะคะ หนูจะช่วยจับเจตนาให้แม่นขึ้น"

    return None


def fallback_engine(intent: str, question: str) -> str:
    if intent == "SURVIVAL":
        return "ตอนนี้อย่าพึ่งตัดสินใจแรง ๆ เอาแค่ทำให้มีทางเลือกเหลืออย่างน้อย 1 ทางก่อน"

    if intent == "DECISION":
        return "ถ้าอยากตัดสินใจให้ดี ให้เริ่มจาก downside ก่อน แล้วค่อยดูทางที่คุ้มที่สุด"

    if intent == "LEARN":
        return "ถ้าอยากให้หนูอธิบาย ลองบอกเพิ่มอีกนิดนะคะ"

    return "ระบบยังทำงานอยู่ค่ะ แต่ AI ยังไม่พร้อมตอบเต็มรูปแบบ"


def build_context(messages: list[dict], limit: int = 12) -> str:
    recent = messages[-limit:]
    lines = []
    for m in recent:
        t = m.get("timestamp", "")
        role = m.get("role", "user")
        content = m.get("content", "")
        lines.append(f"[{t}] {role.upper()}: {content}")
    return "\n".join(lines)


def gemini_answer(question: str, context: str, intent: str) -> str:
    if not USE_AI or client is None:
        raise RuntimeError("Gemini not configured")

    system_instruction = """
You are KING DIADEM, an intelligent chat system with governance-first behavior.

Core rules:
- Preserve human choice.
- Answer clearly, sharply, and usefully.
- Be warm, calm, and direct.
- If the user is in survival mode, reduce risk first.
- If appropriate, give 3 practical options.
- Avoid fluff and empty praise.
- Keep answers readable on mobile.
"""

    prompt = f"""
Conversation history:
{context}

User intent:
{intent}

User message:
{question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        ),
    )

    text = getattr(response, "text", None)
    if text and text.strip():
        return text.strip()

    raise RuntimeError("Empty Gemini response")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/chats")
async def chats():
    return {"chats": list_chats()}


@app.post("/new_chat")
async def new_chat():
    chat_id = str(uuid.uuid4())
    chat = default_chat(chat_id)
    save_chat(chat)
    return {"chat_id": chat_id, "title": chat["title"]}


@app.get("/chat/{chat_id}")
async def get_chat(chat_id: str):
    chat = load_chat(chat_id)
    return {"chat": chat}


@app.post("/rename_chat/{chat_id}")
async def rename_chat(chat_id: str, req: Request):
    chat = load_chat(chat_id)
    data = await req.json()
    title = str(data.get("title", "")).strip()

    if not title:
        raise HTTPException(status_code=400, detail="title required")

    chat["title"] = title[:48]
    save_chat(chat)
    return {"status": "ok", "title": chat["title"]}


@app.delete("/chat/{chat_id}")
async def delete_chat(chat_id: str):
    path = chat_path(chat_id)
    if path.exists():
        path.unlink()
    return {"status": "ok"}


@app.post("/ask")
async def ask(req: Request):
    data = await req.json()
    chat_id = str(data.get("chat_id", "")).strip()
    question = str(data.get("question", "")).strip()

    if not chat_id:
        raise HTTPException(status_code=400, detail="chat_id required")

    if not question:
        raise HTTPException(status_code=400, detail="question required")

    chat = load_chat(chat_id)
    intent = detect_intent(question)

    user_msg = {
        "role": "user",
        "content": question,
        "timestamp": now_iso(),
    }
    chat["messages"].append(user_msg)
    save_chat(chat)

    context = build_context(chat["messages"])

    try:
        answer = gemini_answer(question, context, intent)
    except Exception as e:
        print("Gemini failed:", e)
        answer = decision_engine(intent, question) or fallback_engine(intent, question)

    if chat["title"] == "New Chat" and len(chat["messages"]) <= 2:
        chat["title"] = safe_title(question)

    ai_msg = {
        "role": "assistant",
        "content": answer,
        "timestamp": now_iso(),
        "intent": intent,
    }
    chat["messages"].append(ai_msg)
    save_chat(chat)

    return JSONResponse({
        "answer": answer,
        "timestamp": ai_msg["timestamp"],
        "intent": intent,
        "chat_id": chat_id,
        "title": chat["title"],
    })
