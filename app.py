from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json, os, uuid, hashlib

app = FastAPI()

# ---------------- DATABASE ----------------
USERS_FILE = "data/users.json"
os.makedirs("data", exist_ok=True)

def load_users():
    if not os.path.exists(USERS_FILE): return {}
    try:
        with open(USERS_FILE) as f: return json.load(f)
    except: return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def get_user(api_key):
    users = load_users()
    for email in users:
        if users[email]["api_key"] == api_key:
            return email, users
    return None, users

# ---------------- MODELS ----------------
class Auth(BaseModel):
    email: str
    password: str

class DecisionReq(BaseModel):
    question: str

class TopUpReq(BaseModel):
    amount: int

# ---------------- FRONTEND ----------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>KING DIADEM</title>

<style>
body{
    margin:0;
    background:#343541;
    font-family:sans-serif;
    color:white;
}

#chat{
    height:85vh;
    overflow-y:auto;
    padding:20px;
}

.msg{
    margin:10px 0;
    padding:12px;
    border-radius:10px;
    max-width:80%;
}

.user{
    background:#2563eb;
    margin-left:auto;
}

.bot{
    background:#444654;
}

#input{
    display:flex;
    padding:10px;
    background:#40414f;
}

input{
    flex:1;
    padding:12px;
    border:none;
    border-radius:5px;
}

button{
    margin-left:10px;
    padding:12px;
}
</style>
</head>

<body>

<div id="chat">
<div class="msg bot">ระบบพร้อมใช้งาน</div>
</div>

<div id="input">
<input id="msg" placeholder="พิมพ์..." onkeypress="if(event.key==='Enter')send()">
<button onclick="send()">ส่ง</button>
</div>

<script>

async function send(){
    const input = document.getElementById("msg");
    const chat = document.getElementById("chat");

    const text = input.value.trim();
    if(!text) return;

    chat.innerHTML += `<div class="msg user">${text}</div>`;
    input.value="";

    const res = await fetch("/decision",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "api_key":localStorage.getItem("api_key") || ""
        },
        body:JSON.stringify({question:text})
    });

    const data = await res.json();

    const reply = data.response || data.msg || data.error;

    chat.innerHTML += `<div class="msg bot">${reply}</div>`;
    chat.scrollTop = chat.scrollHeight;
}

</script>

</body>
</html>
"""

# ---------------- AUTH ----------------
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

    if data.email not in users:
        raise HTTPException(401, "Invalid")

    if users[data.email]["password"] != hash_password(data.password):
        raise HTTPException(401, "Invalid")

    return users[data.email]

@app.get("/status")
def status(api_key: str = Header(None)):
    email, users = get_user(api_key)
    if not email:
        raise HTTPException(401, "Invalid Key")

    return {"credits": users[email]["credits"]}

# ---------------- TOPUP ----------------
@app.post("/topup")
def topup(req: TopUpReq, api_key: str = Header(None)):
    email, users = get_user(api_key)

    if not email:
        raise HTTPException(401, "Unauthorized")

    users[email]["credits"] += req.amount
    save_users(users)

    return {"new_balance": users[email]["credits"]}

# ---------------- DECISION CORE ----------------
@app.post("/decision")
def decision(req: DecisionReq, api_key: str = Header(None)):

    email, users = get_user(api_key)

    if not email:
        return {"error": "กรุณาล็อกอินก่อน"}

    if users[email]["credits"] <= 0:
        return {"msg": "เครดิตหมด"}

    users[email]["credits"] -= 1
    save_users(users)

    q = req.question.lower()

    # 🔥 CORE LOGIC (ตรงกับระบบพี่)
    if "เงิน" in q:
        answer = "รักษาทุน ห้ามเสี่ยงเกินตัว"
    elif "เสี่ยง" in q:
        answer = "ลด exposure ก่อน แล้วค่อยขยาย"
    elif "ทางเลือก" in q:
        answer = "ต้องรักษา choice > 0"
    else:
        answer = "เลือกทางที่ยังไม่ปิดอนาคต"

    return {
        "response": answer,
        "credits_left": users[email]["credits"]
    }
