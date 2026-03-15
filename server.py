import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# ENGINE
from ENGINE.decision_engine import run_decision

# AUTH
from AUTH.auth_system import register, login

# PAYMENT
from PAYMENT.wallet_engine import topup

# DATABASE
from DATABASE.user_db import init_db

app = FastAPI(title="KING DIADEM")

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- INIT DATABASE ----------
init_db()

# ---------- STATIC FILES ----------
app.mount("/FRONTEND", StaticFiles(directory="FRONTEND"), name="frontend")


# ==============================
# ROOT
# ==============================

@app.get("/", response_class=HTMLResponse)
def root():
    with open("index.html") as f:
        return f.read()


# ==============================
# AI DECISION
# ==============================

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


# ==============================
# REGISTER
# ==============================

@app.post("/register")
async def api_register(data: dict):

    email = data.get("email")
    password = data.get("password")

    return register(email, password)


# ==============================
# LOGIN
# ==============================

@app.post("/login")
async def api_login(data: dict):

    email = data.get("email")
    password = data.get("password")

    return login(email, password)


# ==============================
# WALLET TOPUP
# ==============================

@app.post("/wallet/topup")
async def api_topup(data: dict):

    email = data.get("email")
    amount = int(data.get("amount"))

    return topup(email, amount)


# ==============================
# HEALTH CHECK
# ==============================

@app.get("/system")
def system():

    return {
        "system": "KING DIADEM",
        "status": "running"
    }
