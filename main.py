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
