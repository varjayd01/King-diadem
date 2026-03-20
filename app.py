from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

import uuid, os, json, datetime
import google.generativeai as genai

# =========================
# 🔐 GEMINI CONFIG
# =========================
API_KEY = os.getenv("GEMINI_API_KEY")

USE_AI = True

if not API_KEY:
    print("❌ No GEMINI_API_KEY → Fallback Mode")
    USE_AI = False
else:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-pro")
    except Exception as e:
        print("❌ Gemini init error:", e)
        USE_AI = False

# =========================
# 🚀 APP INIT
# =========================
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# =========================
# 💾 STORAGE
# =========================
def path(chat_id):
    return f"data/{chat_id}.json"

def load(chat_id):
    if not os.path.exists(path(chat_id)):
        return []
    with open(path(chat_id), "r") as f:
        return json.load(f)

def save(chat_id, data):
    os.makedirs("data", exist_ok=True)
    with open(path(chat_id), "w") as f:
        json.dump(data, f)

# =========================
# 🧠 INTENT ENGINE
# =========================
def intent_engine(q):
    q = q.lower()

    if any(x in q for x in ["ไม่มีทางเลือก", "จน", "แย่", "หมดทาง"]):
        return "SURVIVAL"

    if any(x in q for x in ["ทำยังไง", "ควร", "แนะนำ"]):
        return "DECISION"

    if any(x in q for x in ["คืออะไร", "อธิบาย"]):
        return "LEARN"

    return "GENERAL"

# =========================
# ⚖️ DECISION ENGINE
# =========================
def decision_engine(intent):
    if intent == "SURVIVAL":
        return "เริ่มจากลดความเสี่ยงก่อน แล้วค่อยสร้างทางเลือก"

    if intent == "DECISION":
        return "แยกทางเลือก → ดู downside → เลือกทางที่รอดก่อน"

    if intent == "LEARN":
        return "นี่คือคำอธิบายแบบสั้น กระชับ และใช้ได้จริง"

    return None

# =========================
# 🛟 FALLBACK
# =========================
def fallback_engine():
    return "⚠️ AI ไม่พร้อมใช้งาน แต่ระบบยังคงทำงาน"

# =========================
# 🧠 CONTEXT BUILDER
# =========================
def build_context(messages, limit=10):
    recent = messages[-limit:]
    history = ""

    for m in recent:
        history += f"[{m['time']}] User: {m['q']}\n"
        history += f"[{m['time']}] AI: {m['a']}\n"

    return history

# =========================
# 🌐 ROUTES
# =========================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/new_chat")
async def new_chat():
    return {"chat_id": str(uuid.uuid4())}

@app.get("/chats")
async def chats():
    os.makedirs("data", exist_ok=True)
    return {"chats": [f.replace(".json","") for f in os.listdir("data")]}

@app.get("/chat/{chat_id}")
async def chat(chat_id: str):
    return {"messages": load(chat_id)}

# =========================
# 💥 CORE /ask
# =========================
@app.post("/ask")
async def ask(req: Request):
    data = await req.json()
    chat_id = data["chat_id"]
    q = data["question"]

    now = datetime.datetime.now().strftime("%H:%M")

    logs = load(chat_id)

    intent = intent_engine(q)
    decision = decision_engine(intent)

    context = build_context(logs)

    try:
        if USE_AI:
            prompt = f"""
You are KING DIadem AI.

Conversation history:
{context}

Intent: {intent}

Rules:
- Answer sharp, real, usable
- No fluff
- Focus on survival & decision
- Keep it short but powerful

User: {q}
"""
            response = model.generate_content(prompt)
            ans = response.text if response.text else decision or fallback_engine()
        else:
            ans = decision or fallback_engine()

    except Exception as e:
        print("AI FAIL:", e)
        ans = decision or fallback_engine()

    # 💾 SAVE พร้อมเวลา
    logs.append({
        "q": q,
        "a": ans,
        "time": now
    })
    save(chat_id, logs)

    return JSONResponse({
        "answer": ans,
        "time": now
    })
