import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# KING DIADEM ENGINE
from ENGINE.decision_engine import decision_engine


# --------------------------------------------------
# FASTAPI INITIALIZATION
# --------------------------------------------------

app = FastAPI(
    title="KING DIADEM",
    description="Civilization Decision Infrastructure",
    version="1.0"
)


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class DecisionRequest(BaseModel):
    location: str
    lat: float
    lng: float
    food: str
    money: float
    risk: str
    text: str


class QuestionRequest(BaseModel):
    question: str


# --------------------------------------------------
# ROOT HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "system": "KING DIADEM",
        "status": "running",
        "mode": "civilization decision engine"
    }


# --------------------------------------------------
# MAIN DECISION ENDPOINT
# --------------------------------------------------

@app.post("/decision")
def decision(request: DecisionRequest):

    result = decision_engine(
        request.location,
        request.lat,
        request.lng,
        request.food,
        request.money,
        request.risk,
        request.text
    )

    return result


# --------------------------------------------------
# SIMPLE QUESTION MODE
# --------------------------------------------------

@app.post("/ask")
def ask(request: QuestionRequest):

    result = decision_engine(
        location="unknown",
        lat=0,
        lng=0,
        food="unknown",
        money=0,
        risk="medium",
        text=request.question
    )

    return result


# --------------------------------------------------
# EMERGENCY MODE
# --------------------------------------------------

@app.post("/emergency")
def emergency(request: DecisionRequest):

    result = decision_engine(
        request.location,
        request.lat,
        request.lng,
        request.food,
        request.money,
        request.risk,
        request.text
    )

    result["mode"] = "emergency"

    return result


# --------------------------------------------------
# SERVER START
# --------------------------------------------------

if __name__ == "__main__":

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
