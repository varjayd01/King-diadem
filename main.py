from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import json
import os
import uuid
import hashlib

app = FastAPI()

# -----------------------------
# Static Web Interface
# -----------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")


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
# Root
# -----------------------------

@app.get("/")
def root():
    return {
        "system": "KING DIADEM",
        "status": "online",
        "engine": "active",
        "version": "1.1"
    }


# -----------------------------
# Signup
# -----------------------------

@app.post("/signup")
def signup(data: dict):

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Missing email or password")

    users = load_users()

    if email in users:
        raise HTTPException(status_code=400, detail="User already exists")

    api_key = "kd_" + uuid.uuid4().hex

    users[email] = {
        "password": hash_password(password),
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
def login(data: dict):

    email = data.get("email")
    password = data.get("password")

    users = load_users()

    if email not in users:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if users[email]["password"] != hash_password(password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login success",
        "api_key": users[email]["api_key"],
        "credits": users[email]["credits"]
    }


# -----------------------------
# Decision Engine
# -----------------------------

@app.post("/decision")
def decision(data: dict):

    api_key = data.get("api_key")
    question = data.get("question")

    users = load_users()

    user_email = find_user_by_api(api_key, users)

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

    # Placeholder Decision Engine
    choices = [
        "ทางเลือก A",
        "ทางเลือก B",
        "ทางเลือก C"
    ]

    return {
        "system": "KING DIADEM",
        "question": question,
        "analysis": "กำลังประเมินทางเลือกที่ปลอดภัยที่สุด",
        "choices": choices,
        "credits_left": users[user_email]["credits"]
    }


# -----------------------------
# Topup Credits
# -----------------------------

@app.post("/topup")
def topup(data: dict):

    api_key = data.get("api_key")
    amount = data.get("amount", 10)

    users = load_users()

    user_email = find_user_by_api(api_key, users)

    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid API key")

    users[user_email]["credits"] += amount
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

    situation = data.get("situation")

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
# Future Expansion Hook
# -----------------------------

@app.get("/system/roadmap")
def roadmap():

    return {
        "phase_1": "Decision engine",
        "phase_2": "AI advisory layer",
        "phase_3": "Global node network",
        "phase_4": "DriftZero governance system"
    }
