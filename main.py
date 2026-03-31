from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os
import uuid
import hashlib

app = FastAPI()

# -----------------------------
# Static Web Interface
# -----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root_page():
    return FileResponse("static/index.html")


# -----------------------------
# Database
# -----------------------------
USERS_FILE = "data/users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE) as f:
        return json.load(f)


def save_users(users):
    os.makedirs("data", exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def find_user_by_api(api_key, users):
    for email in users:
        if users[email]["api_key"] == api_key:
            return email
    return None


# -----------------------------
# Schema
# -----------------------------
class AuthInput(BaseModel):
    email: str
    password: str


class DecisionInput(BaseModel):
    api_key: str
    question: str


class TopupInput(BaseModel):
    api_key: str
    amount: int = 10


# -----------------------------
# CORE BRAIN (🔥 จุดสำคัญ)
# -----------------------------
def run_brain(question: str):
    """
    นี่คือสมองกลางของระบบ
    ต่อ AI จริงในอนาคตได้ตรงนี้
    """

    if not question or question.strip() == "":
        return {
            "analysis": "ไม่มีข้อมูลให้วิเคราะห์",
            "choices": []
        }

    # 🔥 ตัวอย่าง logic จริง (ขยายได้)
    if "เสี่ยง" in question:
        return {
            "analysis": "ตรวจพบความเสี่ยง",
            "choices": [
                "หยุดก่อน",
                "ลดความเสี่ยง",
                "หาทางเลือกใหม่"
            ]
        }

    if "เงิน" in question:
        return {
            "analysis": "เกี่ยวข้องกับทรัพยากร",
            "choices": [
                "เก็บเงิน",
                "ลงทุนอย่างระวัง",
                "ลดรายจ่าย"
            ]
        }

    # default
    return {
        "analysis": "กำลังประเมินทางเลือกที่ปลอดภัยที่สุด",
        "choices": [
            "ทางเลือก A",
            "ทางเลือก B",
            "ทางเลือก C"
        ]
    }


# -----------------------------
# Signup
# -----------------------------
@app.post("/signup")
def signup(data: AuthInput):

    users = load_users()

    if data.email in users:
        raise HTTPException(status_code=400, detail="User already exists")

    api_key = "kd_" + uuid.uuid4().hex

    users[data.email] = {
        "password": hash_password(data.password),
        "credits": 10,
        "api_key": api_key
    }

    save_users(users)

    return {
        "message": "User created",
        "api_key": api_key,
        "credits": 10
    }


# -----------------------------
# Login
# -----------------------------
@app.post("/login")
def login(data: AuthInput):

    users = load_users()

    if data.email not in users:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if users[data.email]["password"] != hash_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login success",
        "api_key": users[data.email]["api_key"],
        "credits": users[data.email]["credits"]
    }


# -----------------------------
# Decision Engine (เชื่อม Brain แล้ว)
# -----------------------------
@app.post("/decision")
def decision(data: DecisionInput):

    users = load_users()
    user_email = find_user_by_api(data.api_key, users)

    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if users[user_email]["credits"] <= 0:
        return {
            "message": "Credits หมด",
            "next": "เติมเครดิตก่อนใช้งานต่อ"
        }

    # ใช้เครดิต
    users[user_email]["credits"] -= 1
    save_users(users)

    # 🔥 เรียกสมองจริง
    brain_output = run_brain(data.question)

    return {
        "system": "KING DIADEM",
        "question": data.question,
        "analysis": brain_output["analysis"],
        "choices": brain_output["choices"],
        "credits_left": users[user_email]["credits"]
    }


# -----------------------------
# Topup Credits
# -----------------------------
@app.post("/topup")
def topup(data: TopupInput):

    users = load_users()
    user_email = find_user_by_api(data.api_key, users)

    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid API key")

    users[user_email]["credits"] += data.amount
    save_users(users)

    return {
        "message": "Topup success",
        "credits": users[user_email]["credits"]
    }


# -----------------------------
# Emergency Mode
# -----------------------------
@app.post("/emergency")
def emergency(data: dict):

    situation = data.get("situation", "unknown")

    return {
        "mode": "EMERGENCY",
        "message": "หยุดก่อน 3 นาที แล้วค่อยคิด",
        "situation": situation,
        "steps": [
            "หยุดการตัดสินใจทันที",
            "หายใจลึก 5 ครั้ง",
            "มองหาทางเลือกที่ไม่ทำร้ายใคร"
        ]
    }


# -----------------------------
# Roadmap
# -----------------------------
@app.get("/system/roadmap")
def roadmap():

    return {
        "phase_1": "Decision engine",
        "phase_2": "AI advisory layer",
        "phase_3": "Global node network",
        "phase_4": "DriftZero governance system"
    }
