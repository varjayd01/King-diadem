from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json, os, uuid, hashlib, importlib

# =========================
# OPTIONAL AI (Gemini)
# =========================
try:
    import google.generativeai as genai

    GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

    if GEMINI_KEY:
        genai.configure(api_key=GEMINI_KEY)
        ai_model = genai.GenerativeModel("gemini-1.5-flash")
    else:
        ai_model = None
except:
    ai_model = None

# =========================
# APP
# =========================
app = FastAPI()

# =========================
# STORAGE
# =========================
DATA_DIR = "data"
USERS_FILE = f"{DATA_DIR}/users.json"

os.makedirs(DATA_DIR, exist_ok=True)

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


# =========================
# ENGINE LOADER
# =========================
def load_engine():
    try:
        module = importlib.import_module("ENGINE.decision_engine")
        return module.decision_engine
    except:
        return None


# =========================
# MODELS
# =========================
class Auth(BaseModel):
    email: str
    password: str

class DecisionReq(BaseModel):
    question: str


# =========================
# FRONTEND (Launch UI)
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="background:black;color:#00f2ff;font-family:sans-serif">

    <h1>👑 KING DIADEM</h1>

    <input id="email" placeholder="email"><br>
    <input id="pass" placeholder="password"><br><br>

    <button onclick="signup()">Signup</button>
    <button onclick="login()">Login</button>

    <hr>

    <textarea id="q" placeholder="Ask the system..." style="width:300px;height:100px"></textarea>
    <br>
    <button onclick="send()">EXECUTE</button>

    <pre id="out"></pre>

    <script>

    async function signup(){
        const email = email.value;
        const password = pass.value;

        const res = await fetch("/signup",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body: JSON.stringify({email,password})
        });

        const data = await res.json();
        localStorage.setItem("key", data.api_key);
        alert("created");
    }

    async function login(){
        const email = email.value;
        const password = pass.value;

        const res = await fetch("/login",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body: JSON.stringify({email,password})
        });

        const data = await res.json();
        localStorage.setItem("key", data.api_key);
        alert("login success");
    }

    async function send(){
        const q = document.getElementById("q").value;

        const res = await fetch("/decision",{
            method:"POST",
            headers:{
                "Content-Type":"application/json",
                "api_key": localStorage.getItem("key")
            },
            body: JSON.stringify({question:q})
        });

        const data = await res.json();
        document.getElementById("out").innerText =
            JSON.stringify(data,null,2);
    }

    </script>
    </body>
    </html>
    """


# =========================
# AUTH
# =========================
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


@app.post("/login")
def login(data: Auth):
    users = load_users()

    if data.email not in users:
        raise HTTPException(401, "invalid")

    if users[data.email]["password"] != hash_password(data.password):
        raise HTTPException(401, "invalid")

    return users[data.email]


# =========================
# DECISION CORE
# =========================
@app.post("/decision")
def decision(req: DecisionReq, api_key: str = Header(None)):

    if not api_key:
        return {"error": "no api key"}

    email, users = get_user(api_key)

    if not email:
        raise HTTPException(401, "bad key")

    if users[email]["credits"] <= 0:
        return {"msg": "no credits"}

    users[email]["credits"] -= 1
    save_users(users)

    # ------------------
    # 1. ENGINE
    # ------------------
    engine = load_engine()

    if engine:
        try:
            result = engine(req.question)
            return {
                "source": "ENGINE",
                "result": result,
                "credits_left": users[email]["credits"]
            }
        except:
            pass

    # ------------------
    # 2. GEMINI (LYLA)
    # ------------------
    if ai_model:
        try:
            prompt = f"""
You are LYLA KERNEL inside KING DIADEM system.
Answer like a strategic AI.
Keep it real, short, and survival-focused.

Question: {req.question}
"""
            response = ai_model.generate_content(prompt)

            return {
                "source": "LYLA",
                "response": response.text,
                "credits_left": users[email]["credits"]
            }
        except:
            pass

    # ------------------
    # 3. FALLBACK (ไม่ตาย)
    # ------------------
    text = req.question.lower()

    if "เงิน" in text:
        answer = "เริ่มเล็กก่อน รักษาสภาพคล่อง"
    elif "เสี่ยง" in text:
        answer = "ลดความเสี่ยงก่อน แล้วค่อยขยาย"
    else:
        answer = "อย่าเลือกทางที่ตัดอนาคต"

    return {
        "source": "fallback",
        "response": answer,
        "credits_left": users[email]["credits"]
    }


# =========================
# SYSTEM STATUS
# =========================
@app.get("/system")
def system():
    return {
        "system": "KING DIADEM",
        "status": "ONLINE",
        "engine": "AUTO"
}
