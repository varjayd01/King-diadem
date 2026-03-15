import os
import stripe
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="KING DIADEM V999")

# =========================
# CONFIG
# =========================

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

stripe.api_key = STRIPE_SECRET_KEY

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# STATIC
# =========================

app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# MEMORY DATABASE
# =========================

USERS = {}
WALLETS = {}
TRANSACTIONS = []

# =========================
# ROOT
# =========================

@app.get("/")
def root():

    return {
        "system":"KING DIADEM",
        "version":"V999",
        "status":"running",
        "ai":"online",
        "decision_engine":"active"
    }

# =========================
# SYSTEM STATUS
# =========================

@app.get("/system")
def system():

    return {
        "system":"KING DIADEM",
        "status":"running"
    }

@app.get("/system/health")
def health():

    return {
        "server":"online",
        "ai":"active",
        "wallet":"ready",
        "stripe":"connected"
    }

# =========================
# BRAIN MAP
# =========================

@app.get("/system/brainmap")
def brainmap():

    return {

        "center":"KING DIADEM",

        "nodes":[

            {"name":"AI Brain","status":"active"},
            {"name":"Decision Engine","status":"active"},
            {"name":"Simulation Engine","status":"ready"},
            {"name":"Wallet System","status":"online"},
            {"name":"Global Node Network","status":"scanning"}

        ]

    }

# =========================
# AI STATUS
# =========================

@app.get("/ai/status")
def ai_status():

    return {

        "ai":"online",

        "modules":[
            "decision_engine",
            "strategy_engine",
            "simulation_engine"
        ]

    }

# =========================
# AI BRAIN
# =========================

@app.get("/ai/brain")
def ai_brain():

    return {

        "brain":"KING DIADEM CORE",

        "modules":[

            {
                "name":"decision_engine",
                "status":"active"
            },

            {
                "name":"strategy_engine",
                "status":"active"
            },

            {
                "name":"simulation_engine",
                "status":"ready"
            },

            {
                "name":"entropy_guard",
                "status":"monitoring"
            }

        ]

    }

# =========================
# AI GALAXY
# =========================

@app.get("/ai/galaxy")
def galaxy_nodes():

    return {

        "center":"KING DIADEM",

        "nodes":[

            {"name":"Human Choice","orbit":1},
            {"name":"AI Strategy","orbit":2},
            {"name":"Simulation Engine","orbit":3},
            {"name":"Global Node","orbit":4},
            {"name":"Economic Flow","orbit":5}

        ]

    }

# =========================
# USERS
# =========================

@app.post("/register")
async def register(req: Request):

    data = await req.json()

    email = data["email"]
    password = data["password"]

    USERS[email] = password
    WALLETS[email] = 0

    return {"status":"registered"}

@app.post("/login")
async def login(req: Request):

    data = await req.json()

    email = data["email"]
    password = data["password"]

    if USERS.get(email) != password:
        raise HTTPException(status_code=401)

    return {"status":"login success"}

# =========================
# WALLET
# =========================

@app.get("/wallet/balance")
def wallet_balance(email:str):

    return {

        "email":email,
        "balance":WALLETS.get(email,0)

    }

@app.post("/wallet/topup")
async def wallet_topup(req: Request):

    data = await req.json()

    email = data["email"]
    amount = data["amount"]

    WALLETS[email] = WALLETS.get(email,0) + amount

    TRANSACTIONS.append({
        "email":email,
        "amount":amount,
        "type":"topup"
    })

    return {"wallet":"updated"}

@app.get("/wallet/history")
def wallet_history():

    return {

        "transactions":TRANSACTIONS

    }

# =========================
# FINANCE
# =========================

@app.get("/system/finance")
def finance():

    return {

        "wallet_users":len(WALLETS),

        "transactions":len(TRANSACTIONS),

        "payment":"stripe"

    }

# =========================
# SERVER
# =========================

@app.get("/system/server")
def server():

    return {

        "provider":"render",
        "mode":"free",
        "status":"running",
        "recommendation":"upgrade when >100 users"

    }

# =========================
# DECISION ENGINE
# =========================

@app.post("/decision")
async def decision(req:Request):

    data = await req.json()

    problem = data["problem"]

    return {

        "problem":problem,
        "decision":"simulate possible paths",
        "status":"analysis running"

    }

# =========================
# STRIPE CHECKOUT
# =========================

@app.post("/create-checkout-session")
async def create_checkout():

    try:

        session = stripe.checkout.Session.create(

            payment_method_types=["card"],

            line_items=[{

                "price":STRIPE_PRICE_ID,
                "quantity":1

            }],

            mode="payment",

            success_url="https://king-diadem.onrender.com/static/success.html",

            cancel_url="https://king-diadem.onrender.com/static/cancel.html"

        )

        return {"url":session.url}

    except Exception as e:

        return {"error":str(e)}

# =========================
# STRIPE WEBHOOK
# =========================

@app.post("/stripe-webhook")
async def stripe_webhook(request:Request):

    payload = await request.body()
    sig = request.headers.get("stripe-signature")

    try:

        event = stripe.Webhook.construct_event(
            payload,
            sig,
            STRIPE_WEBHOOK_SECRET
        )

    except Exception as e:

        raise HTTPException(400,str(e))

    if event["type"] == "checkout.session.completed":

        data = event["data"]["object"]

        TRANSACTIONS.append({

            "type":"stripe_payment",
            "session":data["id"]

        })

    return {"received":True}

# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=10000
        )
