from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json, os, uuid, hashlib

from core.brain import run_brain

app = FastAPI()

# static
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")


# db
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

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def find_user(api_key, users):
    for e in users:
        if users[e]["api_key"] == api_key:
            return e
    return None


# schema
class Auth(BaseModel):
    email: str
    password: str

class Decision(BaseModel):
    api_key: str
    question: str


# signup
@app.post("/signup")
def signup(data: Auth):
    users = load_users()

    if data.email in users:
        raise HTTPException(400, "exists")

    api_key = "kd_" + uuid.uuid4().hex

    users[data.email] = {
        "password": hash_password(data.password),
        "credits": 10,
        "api_key": api_key
    }

    save_users(users)

    return {"api_key": api_key}


# login
@app.post("/login")
def login(data: Auth):
    users = load_users()

    if data.email not in users:
        raise HTTPException(401)

    if users[data.email]["password"] != hash_password(data.password):
        raise HTTPException(401)

    return {
        "api_key": users[data.email]["api_key"],
        "credits": users[data.email]["credits"]
    }


# decision
@app.post("/decision")
def decision(data: Decision):

    users = load_users()
    email = find_user(data.api_key, users)

    if not email:
        raise HTTPException(401)

    if users[email]["credits"] <= 0:
        return {"reply": {"text": "เครดิตหมด", "risk": 1, "choices": []}}

    users[email]["credits"] -= 1
    save_users(users)

    brain = run_brain(data.question)

    return {"reply": brain}
