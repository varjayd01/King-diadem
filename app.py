from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

import uuid, os, json
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
# 🧠 FALLBACK ENGINE
# =========================
def fallback_engine(q):
    q = q.lower()

    if "สวัสดี" in q:
        return "สวัสดีครับ 👑 ระบบยังออนไลน์ (Fallback Mode)"

    if "ใคร" in q:
        return "ผมคือ KING DIADEM — ระบบตัดสินใจ ไม่ใช่แค่ AI"

    if "ช่วย" in q:
        return "ตอนนี้ AI อาจมีปัญหา แต่ระบบยังช่วยวิเคราะห์พื้นฐานได้"

    if "ทำไง" in q:
        return "ให้เริ่มจากลดความเสี่ยงก่อน แล้วค่อยขยายทางเลือก"

    return "⚠️ AI ไม่พร้อมใช้งาน แต่ระบบยังทำงานอยู่"

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

@app.post("/ask")
async def ask(req: Request):
    data = await req.json()
    chat_id = data["chat_id"]
    q = data["question"]

    # =========================
    # 🤖 AI + FALLBACK SYSTEM
    # =========================
    try:
        if USE_AI:
            response = model.generate_content(q)
            ans = response.text if response.text else fallback_engine(q)
        else:
            ans = fallback_engine(q)

    except Exception as e:
        print("AI FAIL:", e)
        ans = fallback_engine(q)

    # =========================
    # 💾 SAVE
    # =========================
    logs = load(chat_id)
    logs.append({"q": q, "a": ans})
    save(chat_id, logs)

    return JSONResponse({"answer": ans})
