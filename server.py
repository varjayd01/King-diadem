import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# ------------------------
# 🧠 SURVIVAL ENGINE
# ------------------------
def survival_engine(user_input):

    text = user_input.lower()

    risk_keywords = [
        "ไม่มีเงิน","หมดเงิน","อยากตาย","ฆ่าตัวตาย",
        "ขายตัว","18+","onlyfans","call","เสียว",
        "หนี้","จน","ทางตัน"
    ]

    if any(k in text for k in risk_keywords):

        return {
            "mode": "survival",
            "answer": """
คุณไม่ได้อ่อนแอ
คุณแค่กำลังอยู่ในจุดที่ทางเลือกมันน้อยมาก

[ตอนนี้สำคัญสุด]
อย่าตัดสินใจที่ย้อนกลับไม่ได้

[ทางรอด 24-72 ชม]
- งานรายวัน (ร้านอาหาร / ส่งของ / ล้างจาน)
- งานออนไลน์ง่าย (แอดมิน / พิมพ์งาน / ขายของ)
- ขอความช่วยเหลือจากคนที่ไว้ใจได้

[ทางออกระยะกลาง]
- สร้างรายได้ที่ไม่ต้องแลกตัว
- เริ่ม skill ที่ต่อยอดได้

ระบบนี้ไม่ตัดสินคุณ
แต่จะช่วยให้คุณมี “ทางเลือกมากกว่า 1”
"""
        }

    return None

# ------------------------
# 🤖 NORMAL ENGINE
# ------------------------
def normal_engine(user_input):
    return {
        "mode": "normal",
        "answer": f"""
Strategic Thinking:

1. Avoid irreversible decisions
2. Preserve your options
3. Expand possible paths

Input:
{user_input}
"""
    }

# ------------------------
# 🌐 ROUTES
# ------------------------

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/ask")
async def ask(request: Request):

    data = await request.json()
    q = data.get("question","")

    survival = survival_engine(q)

    if survival:
        return JSONResponse(survival)

    return JSONResponse(normal_engine(q))


# ------------------------
# 💬 CHAT SYSTEM
# ------------------------
messages = []

@app.post("/chat")
async def chat(request: Request):

    data = await request.json()

    messages.append({
        "name": data.get("name","anon"),
        "message": data.get("message","")
    })

    return {"status":"ok"}

@app.get("/messages")
async def get_messages():
    return {"messages":messages}
