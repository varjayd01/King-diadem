from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json, os, uuid, hashlib

app = FastAPI()

# -------------------------
# DATABASE SETUP
# -------------------------
USERS_FILE = "data/users.json"
os.makedirs("data", exist_ok=True)

def load_users():
    if not os.path.exists(USERS_FILE): return {}
    try:
        with open(USERS_FILE) as f: return json.load(f)
    except: return {}

def save_users(users):
    with open(USERS_FILE, "w") as f: json.dump(users, f, indent=2)

def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()

def get_user(api_key):
    users = load_users()
    for email in users:
        if users[email].get("api_key") == api_key: return email, users
    return None, users

# -------------------------
# MODELS
# -------------------------
class Auth(BaseModel):
    email: str
    password: str

class DecisionReq(BaseModel):
    question: str

class TopUpReq(BaseModel):
    amount: int

# -------------------------
# INTERFACE (ALL-IN-ONE)
# -------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>KING DIADEM | SOVEREIGN SYSTEM</title>
        <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY"></script>
        <style>
            :root { --neon: #00f2ff; --royal: #7000ff; --bg: #020617; }
            body { margin:0; font-family:'Segoe UI'; background:var(--bg); color:white; display:flex; height:100vh; overflow:hidden; }
            
            /* Sidebar: Auth & Profile */
            #sidebar { width: 300px; background: rgba(15, 23, 42, 0.9); border-right: 1px solid rgba(255,255,255,0.1); padding: 20px; display:flex; flex-direction:column; }
            .card { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1); }
            input { width: 100%; padding: 10px; margin: 5px 0; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 5px; box-sizing: border-box; }
            button { width: 100%; padding: 10px; margin: 5px 0; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; transition: 0.3s; }
            .btn-primary { background: var(--neon); color: black; }
            .btn-secondary { background: var(--royal); color: white; }
            
            /* Main Content: Maps & Chat */
            #main { flex: 1; display: flex; flex-direction: column; position: relative; }
            #map { height: 40%; width: 100%; border-bottom: 2px solid var(--neon); filter: grayscale(1) invert(1) contrast(1.2); }
            #chat-container { flex: 1; display: flex; flex-direction: column; padding: 20px; overflow: hidden; }
            #chat-box { flex: 1; overflow-y: auto; padding: 10px; display: flex; flex-direction: column; gap: 10px; }
            .msg { padding: 12px 18px; border-radius: 15px; max-width: 80%; line-height: 1.4; }
            .user { align-self: flex-end; background: var(--royal); }
            .bot { align-self: flex-start; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); }
            
            #input-area { display: flex; gap: 10px; padding-top: 10px; }
            #user-q { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid var(--neon); padding: 15px; border-radius: 30px; color: white; outline: none; }
            
            .stat { font-size: 0.9rem; color: var(--neon); margin-top: 10px; text-align: center; }
            #login-section, #profile-section { display: none; }
        </style>
    </head>
    <body>

    <div id="sidebar">
        <h1 style="font-size: 1.5rem; text-align:center; color: var(--neon);">👑 KING DIADEM</h1>
        
        <div id="login-section" style="display: block;">
            <div class="card">
                <h3>ACCESS PANEL</h3>
                <input id="email" placeholder="Email">
                <input id="pass" type="password" placeholder="Password">
                <button class="btn-primary" onclick="authAction('/signup')">SIGN UP</button>
                <button class="btn-secondary" onclick="authAction('/login')">LOG IN</button>
            </div>
        </div>

        <div id="profile-section">
            <div class="card">
                <h3 id="user-display">COMMANDER</h3>
                <div class="stat">CREDITS: <span id="credit-count">0</span> KD</div>
                <hr style="opacity:0.1">
                <button class="btn-primary" onclick="topUp(100)">TOP UP 100 KD</button>
                <button style="background:#ef4444; color:white" onclick="logout()">LOGOUT</button>
            </div>
        </div>
        
        <div class="card" style="font-size: 0.8rem; opacity: 0.6;">
            SYSTEM: ACTIVE<br>
            KERNEL: LYLA_LOGIC_CORE<br>
            STATUS: PROTECTING LIFE
        </div>
    </div>

    <div id="main">
        <div id="map"></div>
        <div id="chat-container">
            <div id="chat-box">
                <div class="msg bot">ระบบพร้อมแล้วค่ะจอมทัพ โปรดระบุพิกัดหรือป้อนคำสั่งวิเคราะห์ตรรกะ</div>
            </div>
            <div id="input-area">
                <input id="user-q" placeholder="วิเคราะห์สถานการณ์..." onkeypress="if(event.key==='Enter') sendDecision()">
                <button class="btn-primary" onclick="sendDecision()" style="width: 100px; border-radius: 30px;">EXECUTE</button>
            </div>
        </div>
    </div>

    <script>
        let map;
        function initMap() {
            map = new google.maps.Map(document.getElementById("map"), {
                center: { lat: 13.7563, lng: 100.5018 },
                zoom: 12,
                styles: [{"elementType":"geometry","stylers":[{"color":"#242f3e"}]},{"elementType":"labels.text.fill","stylers":[{"color":"#746855"}]}]
            });
        }
        window.onload = () => { 
            initMap(); 
            if(localStorage.getItem("api_key")) showProfile();
            else showLogin();
        };

        async function authAction(path) {
            const email = document.getElementById("email").value;
            const password = document.getElementById("pass").value;
            const res = await fetch(path, {
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body: JSON.stringify({email, password})
            });
            const data = await res.json();
            if(res.ok) {
                localStorage.setItem("api_key", data.api_key);
                localStorage.setItem("user_email", email);
                showProfile();
                updateStats(data.credits);
            } else { alert("Error: " + data.detail); }
        }

        function showProfile() {
            document.getElementById("login-section").style.display = "none";
            document.getElementById("profile-section").style.display = "block";
            document.getElementById("user-display").innerText = localStorage.getItem("user_email");
            fetchStats();
        }

        function showLogin() {
            document.getElementById("login-section").style.display = "block";
            document.getElementById("profile-section").style.display = "none";
        }

        function logout() { localStorage.clear(); location.reload(); }

        async function fetchStats() {
            const res = await fetch("/status", {
                headers: {"api_key": localStorage.getItem("api_key")}
            });
            const data = await res.json();
            updateStats(data.credits);
        }

        function updateStats(c) { document.getElementById("credit-count").innerText = c; }

        async function topUp(amt) {
            const res = await fetch("/topup", {
                method: "POST",
                headers: {"Content-Type":"application/json", "api_key": localStorage.getItem("api_key")},
                body: JSON.stringify({amount: amt})
            });
            const data = await res.json();
            updateStats(data.new_balance);
            alert("เติมเงินสำเร็จ! ยอดคงเหลือ: " + data.new_balance);
        }

        async function sendDecision() {
            const q = document.getElementById("user-q").value;
            if(!q) return;
            const box = document.getElementById("chat-box");
            box.innerHTML += `<div class="msg user">${q}</div>`;
            document.getElementById("user-q").value = "";

            const res = await fetch("/decision", {
                method:"POST",
                headers:{"Content-Type":"application/json", "api_key": localStorage.getItem("api_key")},
                body: JSON.stringify({question: q})
            });
            const data = await res.json();
            const reply = data.response || data.error || data.msg;
            box.innerHTML += `<div class="msg bot"><b>DIADEM_LOGIC:</b><br>${reply}</div>`;
            if(data.credits_left !== undefined) updateStats(data.credits_left);
            box.scrollTop = box.scrollHeight;
        }
    </script>
    </body>
    </html>
    """

@app.get("/status")
def get_status(api_key: str = Header(None)):
    email, users = get_user(api_key)
    if not email: raise HTTPException(401, "Invalid Key")
    return {"credits": users[email]["credits"]}

@app.post("/signup")
def signup(data: Auth):
    users = load_users()
    if data.email in users: raise HTTPException(400, "User exists")
    key = "kd_" + uuid.uuid4().hex
    users[data.email] = {"password": hash_password(data.password), "credits": 10, "api_key": key}
    save_users(users)
    return {"api_key": key, "credits": 10}

@app.post("/login")
def login(data: Auth):
    users = load_users()
    if data.email not in users or users[data.email]["password"] != hash_password(data.password):
        raise HTTPException(401, "Invalid credentials")
    return users[data.email]

@app.post("/topup")
def topup(req: TopUpReq, api_key: str = Header(None)):
    email, users = get_user(api_key)
    if not email: raise HTTPException(401, "Unauthorized")
    users[email]["credits"] += req.amount
    save_users(users)
    return {"new_balance": users[email]["credits"]}

@app.post("/decision")
def decision(req: DecisionReq, api_key: str = Header(None)):
    email, users = get_user(api_key)
    if not email: return {"error": "กรุณาล็อกอินก่อนสั่งการค่ะ"}
    if users[email]["credits"] <= 0: return {"msg": "เครดิตไม่พอค่ะ กรุณาเติมเงิน"}
    
    users[email]["credits"] -= 1
    save_users(users)
    
    text = req.question.lower()
    # ตรรกะวิเคราะห์ (สามารถขยายเพิ่มได้)
    if "เงิน" in text: answer = "เริ่มจากรักษาฐานทุนเดิม ห้ามใช้เกินตัว"
    elif "แผน" in text: answer = "เน้นความเสถียร (Stability) มากกว่าการเสี่ยงที่ควบคุมไม่ได้"
    else: answer = "วิเคราะห์แล้ว: ควรเลือกทางที่รักษาทางเลือกในอนาคตไว้ให้มากที่สุด"
    
    return {"response": answer, "credits_left": users[email]["credits"]}
    
