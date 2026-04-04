from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json, os, uuid, hashlib

app = FastAPI()

# -------------------------
# DATABASE
# -------------------------
USERS_FILE = "data/users.json"
os.makedirs("data", exist_ok=True)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def get_user(api_key):
    users = load_users()
    for email in users:
        if users[email]["api_key"] == api_key:
            return email, users
    return None, users

# -------------------------
# MODEL
# -------------------------
class Auth(BaseModel):
    email: str
    password: str

class DecisionReq(BaseModel):
    question: str

# -------------------------
# FRONTEND (UI แบบ ChatGPT)
# -------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    margin:0;
    font-family:sans-serif;
    background:#0b0b0b;
    color:white;
}

.container {
    display:flex;
    flex-direction:column;
    height:100vh;
}

.topbar {
    padding:15px;
    border-bottom:1px solid #222;
    font-size:18px;
    font-weight:bold;
    color:#00f2ff;
}

.chat {
    flex:1;
    overflow:auto;
    padding:15px;
}

.msg {
    margin:10px 0;
    padding:12px;
    border-radius:10px;
    max-width:80%;
}

.user {
    background:#0055ff;
    align-self:flex-end;
}

.bot {
    background:#222;
    align-self:flex-start;
}

.input-area {
    display:flex;
    padding:10px;
    border-top:1px solid #222;
}

textarea {
    flex:1;
    height:50px;
    border-radius:10px;
    border:none;
    padding:10px;
}

button {
    margin-left:10px;
    padding:10px 15px;
    border:none;
    border-radius:10px;
    background:#00f2ff;
    color:black;
    font-weight:bold;
}

.auth {
    padding:10px;
    border-bottom:1px solid #222;
}
</style>
</head>

<body>
<div class="container">

<div class="topbar">👑 KING DIADEM</div>

<div class="auth">
<input id="email" placeholder="email">
<input id="pass" placeholder="password">
<button onclick="signup()">Signup</button>
<button onclick="login()">Login</button>
</div>

<div id="chat" class="chat"></div>

<div class="input-area">
<textarea id="q" placeholder="Ask anything..."></textarea>
<button onclick="send()">Send</button>
</div>

</div>

<script>

function addMsg(text, type){
    const div = document.createElement("div");
    div.className = "msg " + type;
    div.innerText = text;
    document.getElementById("chat").appendChild(div);
    document.getElementById("chat").scrollTop = 999999;
}

async function signup(){
    const email = document.getElementById("email").value;
    const password = document.getElementById("pass").value;

    const res = await fetch("/signup",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({email,password})
    });

    const data = await res.json();

    if(data.api_key){
        localStorage.setItem("key", data.api_key);
        alert("Signup success");
    }else{
        alert(JSON.stringify(data));
    }
}

async function login(){
    const email = document.getElementById("email").value;
    const password = document.getElementById("pass").value;

    const res = await fetch("/login",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({email,password})
    });

    const data = await res.json();

    if(data.api_key){
        localStorage.setItem("key", data.api_key);
        alert("Login success");
    }else{
        alert(JSON.stringify(data));
    }
}

async function send(){

    const key = localStorage.getItem("key");

    if(!key){
        alert("login ก่อน");
        return;
    }

    const q = document.getElementById("q").value;

    addMsg(q,"user");

    const res = await fetch("/decision",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "api_key": key
        },
        body: JSON.stringify({question:q})
    });

    const data = await res.json();

    addMsg(data.response || JSON.stringify(data),"bot");
}

</script>

</body>
</html>
    """

# -------------------------
# SIGNUP
# -------------------------
@app.post("/signup")
def signup(data: Auth):
    users = load_users()

    if data.email in users:
        raise HTTPException(400, "exists")

    key = "kd_" + uuid.uuid4().hex

    users[data.email] = {
        "password": hash_password(data.password),
        "credits": 10,
        "api_key": key
    }

    save_users(users)

    return {"api_key": key, "credits": 10}

# -------------------------
# LOGIN
# -------------------------
@app.post("/login")
def login(data: Auth):
    users = load_users()

    if data.email not in users:
        raise HTTPException(401, "invalid")

    if users[data.email]["password"] != hash_password(data.password):
        raise HTTPException(401, "invalid")

    return users[data.email]

# -------------------------
# DECISION ENGINE
# -------------------------
@app.post("/decision")
def decision(req: DecisionReq, api_key: str = Header(None)):

    if not api_key:
        return {"error":"no api key"}

    email, users = get_user(api_key)

    if not email:
        raise HTTPException(401, "bad key")

    if users[email]["credits"] <= 0:
        return {"response":"เครดิตหมด"}

    users[email]["credits"] -= 1
    save_users(users)

    text = req.question.lower()

    if "เงิน" in text:
        answer = "เริ่มเล็ก รอดก่อน แล้วค่อยขยาย"
    elif "เสี่ยง" in text:
        answer = "ลด risk ก่อน แล้วค่อย move"
    else:
        answer = "เลือกทางที่ไม่ตัดทางเลือกอนาคต"

    return {
        "response": answer,
        "credits_left": users[email]["credits"]
    }
