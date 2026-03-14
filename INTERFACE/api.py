import os
import json
import time
import stripe
import secrets

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from ENGINE.decision_engine import decision_engine
from ENGINE.simulation_engine import run_simulation
from INTERFACE.mobile_node import mobile_report
from core.api_keys import validate_api_key


# -------------------------
# CONFIG
# -------------------------

DATA_DIR = "data"

DECISION_LOG = f"{DATA_DIR}/decisions.json"
API_USAGE = f"{DATA_DIR}/api_usage.json"
API_KEYS = f"{DATA_DIR}/api_keys.json"

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

stripe.api_key = STRIPE_SECRET_KEY

os.makedirs(DATA_DIR, exist_ok=True)


# -------------------------
# FASTAPI
# -------------------------

app = FastAPI(
    title="KING DIADEM",
    docs_url="/docs"
)


# -------------------------
# CORS
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# MODELS
# -------------------------

class DecisionInput(BaseModel):
    location: str
    food: str
    money: int
    risk: str


class NodeInput(BaseModel):
    location: str
    food: str | None = None
    risk: str | None = None


# -------------------------
# UTILS
# -------------------------

def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# -------------------------
# API KEY CHECK
# -------------------------

def check_api_key(api_key: str):

    if not validate_api_key(api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )


# -------------------------
# RATE LIMIT
# -------------------------

def check_rate_limit(api_key):

    limit = 100

    usage = load_json(API_USAGE)
    count = usage.get(api_key, 0)

    if count >= limit:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )

    usage[api_key] = count + 1

    save_json(API_USAGE, usage)


# -------------------------
# LOG
# -------------------------

def log_decision(input_data, result):

    entry = {
        "time": time.time(),
        "input": input_data,
        "result": result
    }

    with open(DECISION_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


# -------------------------
# HOMEPAGE
# -------------------------

@app.get("/", response_class=HTMLResponse)
async def homepage():

    path = "INTERFACE/index.html"

    if os.path.exists(path):
        with open(path) as f:
            return f.read()

    return "<h1>KING DIADEM API</h1>"


# -------------------------
# PUBLIC UI
# -------------------------

@app.get("/ask")
def ask_page():

    return FileResponse("static/ask.html")


# -------------------------
# SYSTEM STATUS
# -------------------------

@app.get("/system")
def system():

    return {
        "system": "KING DIADEM",
        "status": "online",
        "engine": "active",
        "version": "1.1"
    }


# -------------------------
# DECISION ENGINE
# -------------------------

@app.post("/decision")
def decision(
    data: DecisionInput,
    api_key: str = Header(...)
):

    check_api_key(api_key)
    check_rate_limit(api_key)

    result = decision_engine(
        data.location,
        data.food,
        data.money,
        data.risk
    )

    log_decision(data.dict(), result)

    return result


# -------------------------
# SIMULATION
# -------------------------

@app.post("/simulate")
def simulate(
    data: DecisionInput,
    api_key: str = Header(...)
):

    check_api_key(api_key)
    check_rate_limit(api_key)

    result = run_simulation(
        data.location,
        data.food,
        data.money,
        data.risk
    )

    log_decision(data.dict(), result)

    return result


# -------------------------
# MOBILE NODE
# -------------------------

@app.post("/mobile/node")
def mobile_node(
    data: NodeInput,
    api_key: str = Header(...)
):

    check_api_key(api_key)
    check_rate_limit(api_key)

    world = mobile_report(
        data.location,
        data.food,
        data.risk
    )

    return {
        "status": "node registered",
        "world": world
    }


# -------------------------
# STRIPE CHECKOUT
# -------------------------

@app.post("/payment/checkout")
def create_checkout(api_key: str = Header(...)):

    check_api_key(api_key)

    if not STRIPE_PRICE_ID:
        raise HTTPException(
            status_code=500,
            detail="Stripe price not configured"
        )

    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        mode="subscription",

        line_items=[{
            "price": STRIPE_PRICE_ID,
            "quantity": 1
        }],

        success_url="https://king-diadem.onrender.com/success",
        cancel_url="https://king-diadem.onrender.com/cancel"

    )

    return {
        "checkout_url": session.url
    }


# -------------------------
# STRIPE WEBHOOK
# -------------------------

@app.post("/stripe/webhook")
async def stripe_webhook(request: Request):

    payload = await request.body()

    sig_header = request.headers.get("stripe-signature")

    try:

        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            STRIPE_WEBHOOK_SECRET
        )

    except Exception:

        return {"status": "invalid"}

    if event["type"] == "checkout.session.completed":

        api_key = "kd_" + secrets.token_hex(16)

        keys = load_json(API_KEYS)

        keys[api_key] = {
            "created": time.time(),
            "plan": "pro"
        }

        save_json(API_KEYS, keys)

        print("NEW API KEY:", api_key)

    return {"status": "ok"}
