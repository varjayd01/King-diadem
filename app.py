from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

# ===== IMPORT ENGINE =====
from ENGINE.decision_engine import ENGINE_DECISION

app = FastAPI()

# ===== MEMORY =====
users = {}
usage = {}
FREE_LIMIT = 5

# ===== MODEL =====
class Input(BaseModel):
    location: str
    food: str
    money: int
    risk: int
    username: str

# ===== ROUTE ENGINE (ตัวจริงที่พี่ถาม) =====
@app.post("/ENGINE")
def run_engine(data: Input):

    if data.username not in users:
        return {"error": "no user"}

    usage.setdefault(data.username, 0)

    if usage[data.username] >= FREE_LIMIT:
        return {"error": "limit reached"}

    usage[data.username] += 1

    # 🔥 รวม context → ส่งเข้า ENGINE
    text = f"{data.location} {data.food} {data.money} {data.risk}"

    result = ENGINE_DECISION(text)

    return {
        "ENGINE_RESULT": result,
        "used": usage[data.username],
        "limit": FREE_LIMIT
    }

# ===== AUTH =====
@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    if username in users:
        return {"error": "exists"}

    users[username] = password
    usage[username] = 0
    return {"status": "registered"}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username not in users:
        return {"error": "no user"}

    if users[username] != password:
        return {"error": "wrong password"}

    return {"status": "ok"}

# ===== INDEX UI =====
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>KING DIADEM ENGINE</title>
<style>
body { background:black; color:white; font-family:sans-serif; }
input { margin:4px; }
button { margin:6px; }
</style>
</head>
<body>

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
<input id="risk" placeholder="risk"><br>

<button onclick="run()">RUN ENGINE</button>

<pre id="out"></pre>

<script src="/static/app.js"></script>

</body>
</html>
"""

# ===== PORT =====
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
