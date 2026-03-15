import os
import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="KING DIADEM V999")

# ===============================
# STATIC
# ===============================

app.mount("/static", StaticFiles(directory="static"), name="static")

# ===============================
# CORS
# ===============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ===============================
# MEMORY DATABASE
# ===============================

USERS = {}
WALLETS = {}
TRANSACTIONS = []

# Guest limit
GUEST_LIMIT = 5
GUEST_LOG = {}

# ===============================
# ROOT
# ===============================

@app.get("/")
def root():
    return {
        "system": "KING DIADEM",
        "version": "V999",
        "status": "running"
    }

# ===============================
# SYSTEM STATUS
# ===============================

@app.get("/system/health")
def health():

    return {
        "server": "online",
        "ai": "active",
        "wallet": "ready"
    }

@app.get("/system/server")
def server():

    return {
        "mode": "SURVIVAL",
        "max_guest_requests": GUEST_LIMIT
    }

# ===============================
# USER SYSTEM
# ===============================

@app.post("/register")
async def register(req: Request):

    data = await req.json()

    email = data["email"]
    password = data["password"]

    USERS[email] = password
    WALLETS[email] = 0

    return {"status": "registered"}

@app.post("/login")
async def login(req: Request):

    data = await req.json()

    email = data["email"]
    password = data["password"]

    if USERS.get(email) != password:
        raise HTTPException(status_code=401)

    return {"status": "login success"}

# ===============================
# WALLET
# ===============================

@app.get("/wallet/balance")
def wallet_balance(email: str):

    return {
        "email": email,
        "balance": WALLETS.get(email, 0)
    }

@app.get("/wallet/history")
def wallet_history():

    return {
        "transactions": TRANSACTIONS
    }

# ===============================
# AI STATUS
# ===============================

@app.get("/ai/status")
def ai_status():

    return {
        "ai": "online",
        "modules": [
            "decision_engine",
            "strategy_engine",
            "simulation_engine"
        ]
    }

@app.get("/ai/brain")
def ai_brain():

    return {
        "core": "KING DIADEM",
        "modules": [
            "decision_engine",
            "strategy_engine",
            "simulation_engine"
        ],
        "status": "active"
    }

@app.get("/ai/galaxy")
def ai_galaxy():

    return {
        "nodes": [
            {"id": 1, "name": "AI CORE"},
            {"id": 2, "name": "DECISION ENGINE"},
            {"id": 3, "name": "SIMULATION"},
            {"id": 4, "name": "GLOBAL NODE"}
        ]
    }

# ===============================
# GUEST LIMIT SYSTEM
# ===============================

def check_guest(ip):

    now = time.time()

    if ip not in GUEST_LOG:
        GUEST_LOG[ip] = []

    GUEST_LOG[ip] = [
        t for t in GUEST_LOG[ip]
        if now - t < 86400
    ]

    if len(GUEST_LOG[ip]) >= GUEST_LIMIT:
        return False

    GUEST_LOG[ip].append(now)

    return True


# ===============================
# DECISION ENGINE
# ===============================

@app.post("/decision")
async def decision(req: Request):

    ip = req.client.host

    if not check_guest(ip):

        raise HTTPException(
            status_code=429,
            detail="guest limit reached"
        )

    data = await req.json()

    problem = data["problem"]

    return {
        "problem": problem,
        "analysis": "running simulation",
        "possible_paths": [
            "wait",
            "act now",
            "collect more data"
        ]
    }
