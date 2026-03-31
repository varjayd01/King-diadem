from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os
import uuid
import hashlib

from core.brain import run_brain

app = FastAPI()

# -----------------------------
# Static
# -----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")


# -----------------------------
# DB
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

def find_user(api_key, users):
    for email in users:
        if users[email]["api_key"] == api_key:
            return email
    return None


# -----------------------------
# Schema
# -----------------------------
class Auth(BaseModel):
    email: str
    password: str

class Decision(BaseModel):
    api_key: str
    question: str


# -----------------------------
# Auth
# -----------------------------
@app.post("/signup")
def signup(data: Auth):
    users = load_users()

    if data.email in users:
        raise HTTPException(400, "User exists")

    api_key = "kd_" + uuid.uuid4().hex

    users[data.email] = {
        "password": hash_password(data.password),
        "credits": 10,
        "api_key": api_key
    }

    save_users(users)

    return {"api_key": api_key, "credits": 10}


@app.post("/login")
def login(data: Auth):
    users = load_users()

    if data.email not in users:
        raise HTTPException(401, "Invalid")

    if users[data.email]["password"] != hash_password(data.password):
        raise HTTPException(401, "Invalid")

    return {
        "api_key": users[data.email]["api_key"],
        "credits": users[data.email]["credits"]
    }


# -----------------------------
# Decision (🔥 ใช้ Brain จริง)
# -----------------------------
@app.post("/decision")
def decision(data: Decision):
    users = load_users()

    email = find_user(data.api_key, users)

    if not email:
        raise HTTPException(401, "Invalid API key")

    if users[email]["credits"] <= 0:
        return {"reply": "เครดิตหมด"}

    users[email]["credits"] -= 1
    save_users(users)

    brain = run_brain(data.question)

    return {
        "reply": brain,
        "credits_left": users[email]["credits"]
    }
