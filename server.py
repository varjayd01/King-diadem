from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ENGINE.decision_engine import run_decision
from DATABASE.db import init_db
from AUTH.auth import router as auth_router
from PAYMENT.stripe_payment import create_checkout

app = FastAPI()

init_db()

app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class DecisionInput(BaseModel):
    location:str
    food:int
    money:int
    danger:int


@app.get("/")
def root():
    return {"system":"KING DIADEM ONLINE"}


@app.post("/decision")
def decision(data:DecisionInput):

    result = run_decision(
        data.location,
        data.food,
        data.money,
        data.danger
    )

    return {"result":result}


@app.post("/create-checkout")
def checkout():

    url = create_checkout()

    return {"checkout_url":url}
