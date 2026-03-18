import random
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------
# MEMORY (persona)
# -------------------------
user_profiles = {}

# -------------------------
# CRISIS
# -------------------------
CRISIS_WORDS = ["ตาย","ไม่ไหว","หมดทาง","ป่วย","หิว","ไม่มีเงิน"]

def is_crisis(text):
    return any(w in text for w in CRISIS_WORDS)

# -------------------------
# MODE
# -------------------------
def detect_mode(text):
    if "ไลล่า" in text or "altair" in text:
        return "COUNCIL"
    if "expert" in text:
        return "EXPERT"
    if is_crisis(text):
        return "LYLA"
    return "NORMAL"

# -------------------------
# COMPASS
# -------------------------
def compass():
    d=random.choice(["เหนือ","ใต้","ตะวันออก","ตะวันตก"])
    m=random.randint(50,300)
    return f"🧭 ไปทาง{d} {m} เมตร"

# -------------------------
# MODES
# -------------------------
def normal(q):
    return f"""
คิดก่อนทำ:

- เก็บข้อมูล
- อย่าตัดสินใจเร็ว
- รักษาทางเลือกไว้

{compass()}
"""

def lyla(q):
    return f"""
พี่อยู่ตรงนี้นะ

เอาแค่ก้าวต่อไปก่อน

ลองไปในที่มีคน เช่น ร้านสะดวกซื้อ

{compass()}
"""

def council(q):
    return f"""
⚔️ COUNCIL

1 👑 มองความจริง
2 🌿 รักษาชีวิต
3 ✨ มองอีกมุม

{compass()}
"""

def expert(q):
    return f"""
🧠 EXPERT MODE

วิเคราะห์เชิงลึก:

- Root Cause
- Risk Layer
- Hidden cost

ข้อสรุป:
อย่าตัดสินใจจากอารมณ์

{compass()}
"""

# -------------------------
# ASK
# -------------------------
@app.post("/ask")
async def ask(req:Request):

    data=await req.json()
    q=data.get("question","")
    user=data.get("user","default")

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

# -------------------------
# SAVE PERSONA
# -------------------------
@app.post("/save_profile")
async def save_profile(req:Request):
    data=await req.json()
    user_profiles["me"]=data
    return {"status":"saved"}

# -------------------------
# ROOT
# -------------------------
@app.get("/")
async def root():
    with open("static/index.html","r",encoding="utf-8") as f:
        return HTMLResponse(f.read())
