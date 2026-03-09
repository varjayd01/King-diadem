import os
import json
import time

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ENGINE.decision_engine import decision_engine
from INTERFACE.mobile_node import mobile_report
from core.api_keys import validate_api_key


app = FastAPI(
    title="KING DIADEM",
    docs_url="/docs"
)


# ---------------------------
# CORS
# ---------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------
# DATA FILES
# ---------------------------

DECISION_LOG = "data/decisions.json"
API_USAGE = "data/api_usage.json"


# ---------------------------
# INPUT MODELS
# ---------------------------

class DecisionInput(BaseModel):
    location: str
    food: str
    money: int
    risk: str


class NodeInput(BaseModel):
    location: str
    food: str | None = None
    risk: str | None = None


# ---------------------------
# API KEY CHECK
# ---------------------------

def check_api_key(api_key: str):

    if not validate_api_key(api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )


# ---------------------------
# RATE LIMIT
# ---------------------------

def check_rate_limit(api_key):

    limit = 100
    usage = {}

    if os.path.exists(API_USAGE):
        with open(API_USAGE) as f:
            usage = json.load(f)

    count = usage.get(api_key, 0)

    if count >= limit:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )

    usage[api_key] = count + 1

    os.makedirs("data", exist_ok=True)

    with open(API_USAGE, "w") as f:
        json.dump(usage, f)


# ---------------------------
# DECISION LOGGING
# ---------------------------

def log_decision(input_data, result):

    entry = {
        "time": time.time(),
        "input": input_data,
        "result": result
    }

    os.makedirs("data", exist_ok=True)

    with open(DECISION_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ---------------------------
# HOMEPAGE
# ---------------------------

@app.get("/", response_class=HTMLResponse)
async def homepage():

    path = "INTERFACE/index.html"

    if os.path.exists(path):
        with open(path) as f:
            return f.read()

    return "<h1>KING DIADEM API</h1>"


# ---------------------------
# SYSTEM STATUS
# ---------------------------

@app.get("/system")
def system():

    return {
        "system": "KING DIADEM",
        "status": "online",
        "engine": "active",
        "version": "1.0"
    }


# ---------------------------
# DECISION ENGINE
# ---------------------------

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


# ---------------------------
# MOBILE NODE
# ---------------------------

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
import stripe

@app.post("/payment/checkout")
def create_checkout(api_key: str = Header(...)):

check_api_key(api_key)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

session = stripe.checkout.Session.create(
    payment_method_types=["card"],
    mode="subscription",
    line_items=[
        {
            "price": os.getenv("STRIPE_PRICE_ID"),
            "quantity": 1
        }
    ],
    success_url="https://king-diadem.onrender.com/success",
    cancel_url="https://king-diadem.onrender.com/cancel"
)

return {
    "checkout_url": session.url
}
