from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import random

app = FastAPI()

class Scenario(BaseModel):
    location:str
    food:str
    money:str
    risk:str


@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/simulate")
def simulate(data:Scenario):

    actions=[
        "conserve resources",
        "relocate",
        "negotiate",
        "expand supply"
    ]

    best=random.choice(actions)

    alternatives=[
        {"action":a,"expected_score":round(random.uniform(0.4,0.8),2)}
        for a in actions
    ]

    return{
        "best_action":best,
        "score":round(random.uniform(0.6,0.9),2),
        "alternatives":alternatives
    }
