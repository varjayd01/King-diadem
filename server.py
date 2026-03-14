import os
import uvicorn

from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# ENGINE
from ENGINE.decision_engine import run_decision

# DATABASE
from DATABASE.credit_store import use_credit, get_credits

# PAYMENTS
from PAYMENTS.create_checkout import create_checkout
from PAYMENTS.stripe_webhook import handle_webhook


app = FastAPI(title="KING DIADEM")


# =========================
# STATIC
# =========================

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


# =========================
# HOME
# =========================

@app.get("/", response_class=HTMLResponse)
async def home():

    path = "INTERFACE/dashboard.html"

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    return "<h1>KING DIADEM</h1>"


# =========================
# SYSTEM STATUS
# =========================

@app.get("/system")
async def system():

    return {
        "status": "running",
        "engine": "online",
        "payments": "enabled",
        "credits": "active"
    }


# =========================
# DECISION ENGINE
# =========================

@app.post("/decision")
async def decision(
    request: Request,
    api_key: str = Header(...)
):

    body = await request.json()

    credits = get_credits(api_key)

    if credits <= 0:
        raise HTTPException(
            status_code=402,
            detail="No credits"
        )

    use_credit(api_key)

    result = run_decision(body)

    return {
        "decision": result,
        "credits_left": credits - 1
    }


# =========================
# BUY CREDITS
# =========================

@app.get("/buy")
async def buy(api_key: str = Header(...)):

    url = create_checkout(api_key)

    return {
        "checkout_url": url
    }


# =========================
# STRIPE WEBHOOK
# =========================

@app.post("/stripe/webhook")
async def stripe_webhook(request: Request):

    payload = await request.body()

    sig_header = request.headers.get("stripe-signature")

    if sig_header is None:
        raise HTTPException(
            status_code=400,
            detail="Missing Stripe signature"
        )

    result = handle_webhook(payload, sig_header)

    return {
        "status": result
    }


# =========================
# SERVER START
# =========================

if __name__ == "__main__":

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=10000
    )
