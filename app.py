from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json, os, uuid, hashlib

app = FastAPI()

# ===== CORS (สำคัญมาก) =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== DATABASE =====
USERS_FILE = "data/users.json"
os.makedirs("data", exist_ok=True)

def load_users():
    if not os.path.exists(USERS_FILE): return {}
    try:
        with open(USERS_FILE) as f: return json.load(f)
    except: return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def get_user(api_key):
    users = load_users()
    for email in users:
        if users[email].get("api_key") == api_key:
            return email, users
    return None, users

# ===== MODELS =====
class Auth(BaseModel):
    email: str
    password: str

class DecisionReq(BaseModel):
    question: str

# ===== AUTH =====
@app.post("/signup")
def signup(data: Auth):
    users = load_users()
    if data.email in users:
        raise HTTPException(400, "User exists")

    key = "kd_" + uuid.uuid4().hex

    users[data.email] = {
        "password": hash_password(data.password),
        "credits": 10,
        "api_key": key
    }

    save_users(users)
    return {"api_key": key, "credits": 10}

@app.post("/login")
def login(data: Auth):
    users = load_users()

    if data.email not in users or users[data.email]["password"] != hash_password(data.password):
        raise HTTPException(401, "Invalid credentials")

    return users[data.email]

# ===== STATUS =====
@app.get("/status")
def status(api_key: str = Header(None)):
    email, users = get_user(api_key)
    if not email:
        raise HTTPException(401, "Invalid key")

    return {"credits": users[email]["credits"]}

# ===== TOPUP =====
@app.post("/topup")
def topup(amount: dict, api_key: str = Header(None)):
    email, users = get_user(api_key)
    if not email:
        raise HTTPException(401, "Unauthorized")

    amt = amount.get("amount", 0)
    users[email]["credits"] += amt
    save_users(users)

    return {"credits": users[email]["credits"]}

# ===== DECISION =====
@app.post("/decision")
def decision(req: DecisionReq, api_key: str = Header(None)):
    email, users = get_user(api_key)

    if not email:
        return {"response": "กรุณาล็อกอินก่อน"}

    if users[email]["credits"] <= 0:
        return {"response": "เครดิตหมด"}

    users[email]["credits"] -= 1
    save_users(users)

    q = req.question.lower()

    if "เงิน" in q:
        ans = "รักษาเงินก่อน อย่าเสี่ยง"
    elif "เสี่ยง" in q:
        ans = "ลด exposure ก่อน"
    else:
        ans = "เลือกทางที่ยังมีทางหนี"

    return {
        "response": ans,
        "credits": users[email]["credits"]
    }
