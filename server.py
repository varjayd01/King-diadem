import os
import stripe
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# STATIC

app.mount("/static", StaticFiles(directory="static"), name="static")


# STRIPE

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PRICE_PREMIUM = os.getenv("STRIPE_PRICE_ID")
PRICE_PRO = os.getenv("STRIPE_PRICE_PRO")
PRICE_SOVEREIGN = os.getenv("STRIPE_PRICE_SOVEREIGN")


# MEMORY

messages = []


# HOME

@app.get("/")
def home():
    return FileResponse("index.html")


# AI DECISION

@app.post("/ask")
async def ask(data: dict):

    question = data.get("question", "")

    answer = "Strategic response: gather information, avoid irreversible decisions."

    return {
        "answer": answer
    }


# GLOBAL CHAT

@app.post("/world/chat")
async def chat(data: dict):

    messages.append(data)

    return {"status": "ok"}


@app.get("/world/messages")
def get_messages():

    return {
        "messages": messages
    }


# STRIPE CHECKOUT

@app.post("/create-checkout-session")
async def checkout(request: Request):

    data = await request.json()

    plan = data.get("plan")

    price_map = {

        "premium": PRICE_PREMIUM,
        "pro": PRICE_PRO,
        "sovereign": PRICE_SOVEREIGN

    }

    price = price_map.get(plan)

    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        line_items=[{
            "price": price,
            "quantity": 1
        }],

        mode="subscription",

        success_url="https://king-diadem.onrender.com/?success=true",

        cancel_url="https://king-diadem.onrender.com/?cancel=true"

    )

    return {"url": session.url}


# START

if __name__ == "__main__":

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=10000
    )
