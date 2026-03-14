import os
import stripe
import uvicorn

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ENGINE.decision_engine import decision_engine
from AUTH.api_key_manager import validate_api_key, use_credit, add_credit


# ==========================================
# STRIPE CONFIG
# ==========================================

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

if not STRIPE_SECRET_KEY:
    raise Exception("STRIPE_SECRET_KEY missing")

stripe.api_key = STRIPE_SECRET_KEY


# ==========================================
# FASTAPI INIT
# ==========================================

app = FastAPI(
    title="KING DIADEM",
    version="1.0"
)


# ==========================================
# REQUEST MODEL
# ==========================================

class DecisionRequest(BaseModel):
    location: str
    food: int
    money: int
    risk: str


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():
    return {
        "system": "KING DIADEM",
        "status": "running"
    }


# ==========================================
# STATUS
# ==========================================

@app.get("/status")
def status():
    return {
        "system": "KING DIADEM",
        "status": "online",
        "engine": "decision-core"
    }


# ==========================================
# HEALTH
# ==========================================

@app.get("/health")
def health():
    return {"health": "ok"}


# ==========================================
# DASHBOARD
# ==========================================

@app.get("/dashboard")
def dashboard():
    return FileResponse("INTERFACE/dashboard.html")


# ==========================================
# DECISION API
# ==========================================

@app.post("/decision")
async def decision(req: DecisionRequest, api_key: str = Header(...)):

    try:

        if not validate_api_key(api_key):
            raise HTTPException(status_code=403, detail="Invalid API key")

        if not use_credit(api_key):
            raise HTTPException(status_code=402, detail="No credits")

        result = decision_engine(
            req.location,
            13.7,
            100.5,
            int(req.food),
            int(req.money),
            req.risk
        )

        return {
            "system": "KING DIADEM",
            "decision": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# BUY CREDITS
# ==========================================

@app.get("/buy-credits")
def buy_credits(api_key: str):

    try:

        session = stripe.checkout.Session.create(

            payment_method_types=["card"],

            client_reference_id=api_key,

            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "KING DIADEM CREDITS"
                    },
                    "unit_amount": 500
                },
                "quantity": 1
            }],

            mode="payment",

            success_url="https://king-diadem.onrender.com/success",
            cancel_url="https://king-diadem.onrender.com/cancel"

        )

        return {"payment_url": session.url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# STRIPE WEBHOOK
# ==========================================

@app.post("/stripe-webhook")
async def stripe_webhook(request: Request):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:

        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            WEBHOOK_SECRET
        )

    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        api_key = session.get("client_reference_id")

        if api_key:
            add_credit(api_key, 10)

    return {"status": "ok"}


# ==========================================
# PAYMENT SUCCESS
# ==========================================

@app.get("/success")
def payment_success():
    return {"status": "payment success"}


# ==========================================
# PAYMENT CANCEL
# ==========================================

@app.get("/cancel")
def payment_cancel():
    return {"status": "payment cancelled"}


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=10000
    )
