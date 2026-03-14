import uvicorn
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from ENGINE.decision_engine import decision_engine
from AUTH.api_key_manager import validate_api_key,use_credit

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
def decision(req:DecisionRequest, api_key:str = Header(...)):

    if not validate_api_key(api_key):
        raise HTTPException(status_code=403,detail="Invalid API KEY")

    if not use_credit(api_key):
        raise HTTPException(status_code=402,detail="No credits")

    result = decision_engine(
        req.location,
        13.7,
        100.5,
        req.food,
        req.money,
        req.risk
    )

    return result


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=10000
    )
from PAYMENT.stripe_payment import create_payment_session

@app.get("/buy-credits")
def buy_credits():
    url = create_payment_session()
    return {"payment_url": url}
