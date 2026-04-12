from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import os

# ✅ IMPORTANT: ใช้ ENGINE ตัวใหญ่ให้ตรงโฟลเดอร์จริง
from ENGINE.decision_engine import KingDiademEngine

app = FastAPI()

# =========================
# ENGINE INIT
# =========================
engine = KingDiademEngine()

# =========================
# STATIC + TEMPLATE
# =========================
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")

# =========================
# MOCK DATABASE (กันพัง)
# =========================
users = {"admin": "1234"}
usage = {}

FREE_LIMIT = 100

# =========================
# INPUT MODEL
# =========================
class Input(BaseModel):
    username: str
    location: str
    food: str
    money: str
    risk: str

# =========================
# ROOT (แก้ BUG JINJA ตรงนี้)
# =========================
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}   # ✅ ห้ามแก้รูปแบบนี้เด็ดขาด
    )

# =========================
# REGISTER
# =========================
@app.post("/register")
def register(username: str, password: str):
    if username in users:
        return {"error": "user exists"}

    users[username] = password
    return {"status": "registered"}

# =========================
# LOGIN
# =========================
@app.post("/login")
def login(username: str, password: str):
    if users.get(username) != password:
        return {"error": "invalid login"}

    return {"status": "ok"}

# =========================
# ENGINE (ตัวหลัก)
# =========================
@app.post("/ENGINE")
def run_engine(data: Input):

    # ตรวจ user
    if data.username not in users:
        return {"error": "no user"}

    # limit usage
    usage.setdefault(data.username, 0)

    if usage[data.username] >= FREE_LIMIT:
        return {"error": "limit reached"}

    usage[data.username] += 1

    # รวม input
    text = f"{data.location} {data.food} {data.money} {data.risk}"

    try:
        # ✅ เรียก ENGINE จริง
        result = engine.run(text)

    except Exception as e:
        return {"error": str(e)}

    return {
        "status": "ok",
        "input": text,
        "result": result
    }
