from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from passlib.context import CryptContext

# ===== ENGINE IMPORT (สำคัญ) =====
from ENGINE.decision_engine import ENGINE_DECISION

app = FastAPI()

# ===== AUTH =====
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {}
usage = {}
FREE_LIMIT = 5

def hash_password(pw):
    return pwd_context.hash(pw)

def verify(pw, hashed):
    return pwd_context.verify(pw, hashed)

# ===== INPUT =====
class Input(BaseModel):
    location: str
    food: str
    money: int
    risk: int
    username: str

# ===== ENGINE ROUTE =====
@app.post("/ENGINE")
def run_engine(data: Input):

    if data.username not in users:
        return {"error": "no user"}

    usage.setdefault(data.username, 0)

    if usage[data.username] >= FREE_LIMIT:
        return {"error": "limit reached"}

    usage[data.username] += 1

    text = f"{data.location} {data.food} {data.money} {data.risk}"

    result = ENGINE_DECISION(text)

    return {
        "result": result,
        "used": usage[data.username],
        "limit": FREE_LIMIT
    }

# ===== REGISTER =====
@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    if username in users:
        return {"error": "exists"}

    users[username] = hash_password(password)
    usage[username] = 0

    return {"status": "registered"}

# ===== LOGIN =====
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username not in users:
        return {"error": "no user"}

    if not verify(password, users[username]):
        return {"error": "wrong password"}

    return {"status": "ok"}

# ===== UI =====
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>KING DIADEM</title>
    </head>
    <body style="background:black;color:white;font-family:sans-serif">

    <h2>⚔️ KING DIADEM ENGINE</h2>

    <h3>สมัคร</h3>
    <input id="r_user" placeholder="user">
    <input id="r_pass" placeholder="pass">
    <button onclick="reg()">Register</button>

    <h3>ล็อกอิน</h3>
    <input id="l_user" placeholder="user">
    <input id="l_pass" placeholder="pass">
    <button onclick="login()">Login</button>

    <h3>ENGINE</h3>
    <input id="location" placeholder="location"><br>
    <input id="food" placeholder="food"><br>
    <input id="money" placeholder="money"><br>
    <input id="risk" placeholder="risk"><br><br>

    <button onclick="run()">RUN ENGINE</button>

    <pre id="out"></pre>

    <script src="/static/app.js"></script>

    </body>
    </html>
    """
