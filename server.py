import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from ENGINE.decision_engine import decision_engine

app = FastAPI(
    title="KING DIADEM",
    version="1.0"
)

class DecisionRequest(BaseModel):

    location:str
    food:int
    money:int
    risk:str

@app.get("/")
def root():

    return {
        "system":"KING DIADEM",
        "status":"running"
    }

@app.post("/decision")
def decision(req:DecisionRequest):

    result = decision_engine(
        req.location,
        13.7,
        100.5,
        req.food,
        req.money,
        req.risk,
        ""
    )

    return result


if __name__ == "__main__":

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=10000
    )
