from fastapi import FastAPI, HTTPException
import json
import os
import uuid
import hashlib

app = FastAPI()

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


@app.get("/")
def root():
    return {"message": "KING DIADEM online"}


@app.post("/signup")
def signup(data: dict):

    email = data.get("email")
    password = data.get("password")

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
        "api_key": api_key
    }


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
        "api_key": users[email]["api_key"]
    }

@app.post("/decision")
def decision(data: dict):

    api_key = data.get("api_key")
    question = data.get("question")

    users = load_users()

    user_email = None

    for email in users:
        if users[email]["api_key"] == api_key:
            user_email = email
            break

    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if users[user_email]["credits"] <= 0:
        return {
            "message": "Creditsหมดแล้ว",
            "next": "เติมเงิน 5 บาทเพื่อถามต่อ"
        }

    users[user_email]["credits"] -= 1
    save_users(users)

    return {
        "king": "ผมกำลังวิเคราะห์ทางเลือกให้ครับ",
        "question": question,
        "choices": [
            "ทางเลือก A",
            "ทางเลือก B",
            "ทางเลือก C"
        ],
        "credits_left": users[user_email]["credits"]
    }
