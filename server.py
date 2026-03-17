import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# serve static
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------
# 🧠 MEMORY (ง่ายๆก่อน)
# -------------------------
chat_memory = []

# -------------------------
# ⚠️ CRISIS DETECTION
# -------------------------
CRISIS_WORDS = [
    "ตาย", "ฆ่าตัวตาย", "ไม่ไหว", "หมดทาง",
    "ป่วย", "หิว", "ไม่มีเงิน", "ช่วยด้วย"
]

def is_crisis(text):
    return any(word in text for word in CRISIS_WORDS)

# -------------------------
# 🧠 MODE DETECTION
# -------------------------
def detect_mode(text):
    text = text.lower()

    if "ไลล่า" in text or "altair" in text or "เวก้า" in text:
        return "COUNCIL"

    if is_crisis(text):
        return "LYLA"

    return "NORMAL"

# -------------------------
# 🧭 COMPASS ENGINE
# -------------------------
import random

def generate_direction():
    dirs = ["เหนือ", "ใต้", "ตะวันออก", "ตะวันตก"]
    d = random.choice(dirs)
    meters = random.randint(50, 500)

    return f"🧭 เดินไปทาง{d}ประมาณ {meters} เมตร เพื่อหาทางเลือกที่ดีกว่า"

# -------------------------
# 🌿 LYLA MODE (ช่วยชีวิต)
# -------------------------
def lyla_response(q):

    if "ป่วย" in q:
        action = "ลองไปหาร้านยาใกล้ตัว หรือคลินิกที่เปิดอยู่ก่อนนะคะ"
    elif "หิว" in q:
        action = "ลองหาร้านข้าวราคาถูก หรือร้านสะดวกซื้อใกล้ตัวก่อนนะคะ"
    elif "ไม่มีเงิน" in q:
        action = "ลองหางานเล็กๆระยะสั้น หรือขอความช่วยเหลือจากคนใกล้ตัวก่อนนะคะ"
    else:
        action = "ลองไปอยู่ในที่ที่ปลอดภัยและมีคน เช่น ร้านสะดวกซื้อ หรือพื้นที่สาธารณะก่อนนะคะ"

    return f"""
ตอนนี้พี่ยังอยู่ตรงนี้นะคะ

ไม่ต้องรีบแก้ทุกอย่างทีเดียว
เอาแค่ก้าวต่อไปก่อน

👉 {action}

{generate_direction()}
"""

# -------------------------
# ⚔️ COUNCIL MODE (3 ทางเลือก)
# -------------------------
def council_response(q):

    king = f"👑 King: มองความจริงก่อน แล้วเลือกทางที่ยังเดินต่อได้"
    lyla = f"🌿 Lyla: เลือกทางที่ทำให้คุณยังปลอดภัย และมีลมหายใจต่อ"
    altair = f"✨ Altair: ลองมองอีกมุม อาจมีทางที่คุณยังไม่เห็น"

    direction = generate_direction()

    return f"""
⚔️ COUNCIL ACTIVE

คุณมี 3 ทางเลือก:

1️⃣ {king}

2️⃣ {lyla}

3️⃣ {altair}

ไม่ว่าคุณจะเลือกทางไหน
สิ่งสำคัญคือ “ยังมีทางให้เดินต่อ”

{direction}
"""

# -------------------------
# 👑 NORMAL MODE
# -------------------------
def normal_response(q):

    return f"""
Strategic Response:

- Gather more information
- Avoid irreversible decisions
- Keep at least one safe option

{generate_direction()}
"""

# -------------------------
# 🧠 MAIN AI ENDPOINT
# -------------------------
@app.post("/ask")
async def ask(request: Request):

    data = await request.json()
    question = data.get("question", "")

    mode = detect_mode(question)

    if mode == "LYLA":
        answer = lyla_response(question)

    elif mode == "COUNCIL":
        answer = council_response(question)

    else:
        answer = normal_response(question)

    chat_memory.append({
        "q": question,
        "mode": mode
    })

    return JSONResponse({"answer": answer})

# -------------------------
# 🌍 CHAT
# -------------------------
@app.post("/chat")
async def chat(request: Request):

    data = await request.json()
    name = data.get("name")
    message = data.get("message")

    chat_memory.append({
        "name": name,
        "message": message
    })

    return JSONResponse({"status": "ok"})

# -------------------------
# 🏠 ROOT
# -------------------------
@app.get("/")
async def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())
