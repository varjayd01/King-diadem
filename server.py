import os
import stripe

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


messages=[]


stripe.api_key=os.getenv("STRIPE_SECRET_KEY")
PRICE_ID=os.getenv("STRIPE_PRICE_ID")


@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/ask")
async def ask(data:dict):

    q=data["question"]

    answer="Strategic response: gather information, avoid irreversible decisions."

    return {"answer":answer}


@app.post("/world/chat")
async def chat(data:dict):

    messages.append(data)

    return {"status":"ok"}


@app.get("/world/messages")
def get_messages():

    return {"messages":messages}


@app.post("/create-checkout-session")
def checkout():

    session=stripe.checkout.Session.create(

        payment_method_types=["card"],

        line_items=[{
