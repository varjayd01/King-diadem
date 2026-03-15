import os
import json
import stripe
import uvicorn
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ==============================
# CONFIG
# ==============================

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

stripe.api_key = STRIPE_SECRET_KEY

# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# STATIC
# ==============================

app.mount("/static", StaticFiles(directory="static"), name="static")

# ==============================
# DATABASE (simple memory)
# ==============================

USERS = {}
WALLET = {}
TRANSACTIONS = []

# ==============================
# ROOT
# ==============================

@app.get("/")
def root():
    return {"system":"KING DIADEM","status":"running"}

# ==============================
# SYSTEM
# ==============================

@app.get("/system")
def system_status():
    return {
        "system":"KING DIADEM",
        "status":"running"
    }

@app.get("/system/health")
def system_health():
    return {
        "system":"KING DIADEM",
        "status":"running",
        "ai":"active",
        "wallet":"ready",
        "stripe":"connected"
    }

# ==============================
# AUTH
# ==============================

@app.post("/register")
async def register(req: Request):
    data = await req.json()
    email = data["email"]
    password = data["password"]

    USERS[email] = password
    WALLET[email] = 0

    return {"status":"registered"}

@app.post("/login")
async def login(req: Request):
    data = await req.json()
    email = data["email"]
    password = data["password"]

    if USERS.get(email) != password:
        raise HTTPException(401)

    return {"status":"login success"}

# ==============================
# WALLET
# ==============================

@app.get("/wallet/balance")
def wallet_balance(email:str):

    balance = WALLET.get(email,0)

    return {
        "email":email,
        "balance":balance
    }

@app.get("/wallet/history")
def wallet_history():

    return {
        "transactions":TRANSACTIONS
    }

@app.post("/wallet/topup")
async def wallet_topup(req:Request):

    data = await req.json()

    email = data["email"]
    amount = data["amount"]

    WALLET[email] = WALLET.get(email,0) + amount

    TRANSACTIONS.append({
        "email":email,
        "amount":amount,
        "type":"topup"
    })

    return {"status":"wallet updated"}

# ==============================
# STRIPE CHECKOUT
# ==============================

@app.post("/create-checkout-session")
async def create_checkout_session():

    try:

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': STRIPE_PRICE_ID,
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://king-diadem.onrender.com/success',
            cancel_url='https://king-diadem.onrender.com/cancel',
        )

        return {"checkout_url":session.url}

    except Exception as e:

        return {"error":str(e)}

# ==============================
# STRIPE WEBHOOK
# ==============================

@app.post("/stripe-webhook")
async def stripe_webhook(request: Request):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:

        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )

    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        TRANSACTIONS.append({
            "type":"stripe_payment",
            "session":session["id"]
        })

    return {"received":True}

# ==============================
# AI SYSTEM
# ==============================

@app.get("/ai/brain")
def ai_brain():

    return {
        "AI":"KING DIADEM",
        "brain":"online",
        "modules":[
            "decision_engine",
            "simulation_engine",
            "strategy_engine"
        ]
    }

@app.get("/ai/decision")
def ai_decision():

    return {
        "decision_nodes":[
            "risk",
            "reward",
            "survival",
            "probability"
        ]
    }

@app.get("/ai/simulation")
def ai_simulation():

    return {
        "simulation":"running",
        "model":"world_model_v1"
    }

# ==============================
# SERVER START
# ==============================

if __name__ == "__main__":

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=10000,
        reload=True
        )
