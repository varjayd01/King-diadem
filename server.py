from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import stripe
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PRICE_ID = os.getenv("STRIPE_PRICE_ID")

@app.get("/")
def root():

    return {"system":"KING DIADEM ONLINE"}

@app.get("/health")
def health():

    return {"status":"ok"}

@app.post("/decision")
async def decision(request: Request):

    body = await request.json()

    location = body.get("location","unknown")
    food = int(body.get("food",0))
    money = int(body.get("money",0))
    risk = int(body.get("risk",0))

    score = max(0,min(100,(food*2)+(money/10)-(risk*3)))

    if score > 70:
        action = "Advance strategic position"
    elif score > 40:
        action = "Stabilize resources"
    else:
        action = "Minimize exposure and survive"

    return {
        "best_action": action,
        "score": score
    }

@app.post("/create-checkout")
def create_checkout():

    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        line_items=[{
            "price": PRICE_ID,
            "quantity": 1
        }],

        mode="payment",

        success_url="https://varjayd01.github.io/King-diadem/success.html",

        cancel_url="https://varjayd01.github.io/King-diadem/"

    )

    return {"url": session.url}
