from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json, os, uuid, hashlib

app = FastAPI()

-------------------------

DATABASE

-------------------------

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

-------------------------

MODEL

-------------------------

class Auth(BaseModel):
email: str
password: str

class DecisionReq(BaseModel):
question: str

-------------------------

FRONTEND (รวมทุกอย่าง)

-------------------------

@app.get("/", response_class=HTMLResponse)
def home():
return """
<html>
<body style="font-family:sans-serif;background:black;color:white">

<h2>KING DIADEM</h2>  

<input id="email" placeholder="email"><br>  
<input id="pass" placeholder="password"><br><br>  

<button onclick="signup()">Signup</button>  
<button onclick="login()">Login</button>  

<hr>  

<textarea id="q" placeholder="ถาม..." style="width:300px;height:100px"></textarea>  
<br>  
<button onclick="send()">SEND</button>  

<pre id="out"></pre>  

<script>  

async function signup(){  
    const email = document.getElementById("email").value;  
    const password = document.getElementById("pass").value;  

    const res = await fetch("/signup",{  
        method:"POST",  
        headers:{"Content-Type":"application/json"},  
        body: JSON.stringify({email,password})  
    });  

    const data = await res.json();  

    localStorage.setItem("key", data.api_key);  
    alert("Signup success");  
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

    localStorage.setItem("key", data.api_key);  
    alert("Login success");  
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

-------------------------

SIGNUP

-------------------------

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

-------------------------

LOGIN

-------------------------

@app.post("/login")
def login(data: Auth):
users = load_users()

if data.email not in users:  
    raise HTTPException(401, "invalid")  

if users[data.email]["password"] != hash_password(data.password):  
    raise HTTPException(401, "invalid")  

return users[data.email]

-------------------------

DECISION

-------------------------

@app.post("/decision")
def decision(req: DecisionReq, api_key: str = Header(None)):

if not api_key:  
    return {"error":"no api key (login first)"}  

email, users = get_user(api_key)  

if not email:  
    raise HTTPException(401, "bad key")  

if users[email]["credits"] <= 0:  
    return {"msg":"no credits"}  

users[email]["credits"] -= 1  
save_users(users)  

text = req.question.lower()  

if "เงิน" in text:  
    answer = "เริ่มจากเงินเล็กก่อน อย่าฝืนเสี่ยงใหญ่"  
elif "เสี่ยง" in text:  
    answer = "ลดความเสี่ยงก่อน แล้วค่อยขยับ"  
else:  
    answer = "เลือกทางที่ยังเหลือทางเลือกในอนาคต"  

return {  
    "response": answer,  
    "credits_left": users[email]["credits"]  
}
