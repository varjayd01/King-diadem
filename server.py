import random
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

user_profiles = {}

CRISIS_WORDS = ["ตาย","ไม่ไหว","หมดทาง","ป่วย","หิว","ไม่มีเงิน"]

def is_crisis(text):
    return any(w in text for w in CRISIS_WORDS)

def detect_mode(text):
    t=text.lower()
    if "ไลล่า" in t or "altair" in t:
        return "COUNCIL"
    if "expert" in t or "ลึก" in t:
        return "EXPERT"
    if is_crisis(text):
        return "LYLA"
    return "NORMAL"

def compass():
    d=random.choice(["เหนือ","ใต้","ตะวันออก","ตะวันตก"])
    m=random.randint(50,300)
    return f"🧭 ไปทาง{d} {m} เมตร"

def navigation(q):
    if "หิว" in q:
        return "🍜 เปิด Google Maps แล้วค้นหา: ร้านอาหารใกล้ฉัน"
    if "ป่วย" in q:
        return "🏥 ไปคลินิกหรือร้านยาใกล้คุณ"
    return ""

def persona_tone():
    profile=user_profiles.get("me",{})
    style=profile.get("style","ปกติ")

    if "สนุก" in style:
        return "วันนี้ต้องปังนะคะ 🔥"
    elif "ลึก" in style:
        return "ลองมองลึกลงไปนะคะ 🧠"
    return "ค่อยๆคิดนะคะ 🌿"

def normal(q):
    return f"""
{persona_tone()}

- อย่าปิดทางเลือก
- คิดก่อนทำ

{compass()}
{navigation(q)}
"""

def lyla(q):
    return f"""
หนูอยู่ตรงนี้นะคะ 🤍

เอาแค่ก้าวต่อไปก่อน

ลองไปในที่มีคน เช่น ร้านสะดวกซื้อ

{compass()}
{navigation(q)}
"""

def council(q):
    return f"""
⚔️ COUNCIL MODE

👑 King
🌿 Lyla
✨ Altair

เลือกทางที่ยัง “มีชีวิตต่อ”

{compass()}
"""

def expert(q):
    return f"""
🧠 EXPERT MODE

- วิเคราะห์ต้นเหตุ
- ดูความเสี่ยง
- มองผลระยะยาว

{compass()}
"""

@app.post("/ask")
async def ask(req:Request):
    data=await req.json()
    q=data.get("question","")

    mode=detect_mode(q)

    if mode=="LYLA":
        ans=lyla(q)
    elif mode=="COUNCIL":
        ans=council(q)
    elif mode=="EXPERT":
        ans=expert(q)
    else:
        ans=normal(q)

    return JSONResponse({"answer":ans})

@app.post("/save_profile")
async def save_profile(req:Request):
    data=await req.json()
    user_profiles["me"]=data
    return {"status":"saved"}

@app.get("/")
async def root():
    with open("static/index.html","r",encoding="utf-8") as f:
        return HTMLResponse(f.read())
