import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# ===============================
# ENGINE
# ===============================

from ENGINE.decision_engine import run_decision

# ===============================
# AUTH
# ===============================

from AUTH.auth_system import register, login

# ===============================
# PAYMENT
# ===============================

from PAYMENT.wallet_engine import topup

# ===============================
# DATABASE
# ===============================

from DATABASE.user_db import init_db

# ===============================
# APP
# ===============================

app = FastAPI(title="KING DIADEM V999")

# ===============================
# CORS
# ===============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# INIT DATABASE
# ===============================

init_db()

# ===============================
# STATIC FILES
# ===============================

if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# ===============================
# ROOT
# ===============================

@app.get("/", response_class=HTMLResponse)
def root():
    with open("index.html") as f:
        return f.read()

# ===============================
# LOGIN PAGE
# ===============================

@app.get("/login.html", response_class=HTMLResponse)
def login_page():
    with open("login.html") as f:
        return f.read()

# ===============================
# REGISTER PAGE
# ===============================

@app.get("/register.html", response_class=HTMLResponse)
def register_page():
    with open("register.html") as f:
        return f.read()

# ===============================
# WALLET PAGE
# ===============================

@app.get("/wallet.html", response_class=HTMLResponse)
def wallet_page():
    with open("wallet.html") as f:
        return f.read()

# ===============================
# DECISION ENGINE
# ===============================

@app.post("/decision")
async def decision(data: dict):

    location = data.get("location", "")
    food = int(data.get("food", 0))
    money = int(data.get("money", 0))
    danger = int(data.get("danger", 0))

    result = run_decision(location, food, money, danger)

    return {
        "result": result
    }

# ===============================
# REGISTER
# ===============================

@app.post("/register")
async def api_register(data: dict):

    email = data.get("email")
    password = data.get("password")

    return register(email, password)

# ===============================
# LOGIN
# ===============================

@app.post("/login")
async def api_login(data: dict):

    email = data.get("email")
    password = data.get("password")

    return login(email, password)

# ===============================
# WALLET TOPUP
# ===============================

@app.post("/wallet/topup")
async def api_topup(data: dict):

    email = data.get("email")
    amount = int(data.get("amount"))

    return topup(email, amount)

# ===============================
# SYSTEM STATUS
# ===============================

@app.get("/system")
def system():

    return {
        "system": "KING DIADEM",
        "version": "V999",
        "status": "running",
        "ai": "online",
        "decision_engine": "active"
    }

# ===============================
# AI STATUS
# ===============================

@app.get("/ai/status")
def ai_status():

    return {
        "brain": "operational",
        "strategy_engine": "ready",
        "simulation_layer": "ready"
    }

# ===============================
# HEALTH CHECK
# ===============================

@app.get("/health")
def health():

    return {
        "server": "alive",
        "database": "connected",
        "deploy": "render"
    }

# ===============================
# FUTURE APP API
# ===============================

@app.get("/app/info")
def app_info():

    return {
        "name": "KING DIADEM",
        "type": "AI Strategic System",
        "mode": "PWA + Android",
        "status": "beta"
    }

# ===============================
# RUN
# ===============================

if __name__ == "__main__":

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=10000,
        reload=True
    )
