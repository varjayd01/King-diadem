from fastapi import FastAPI
from ENGINE.decision_engine import generate_choices

app = FastAPI()

@app.get("/")
def root():
    return {"system": "KING DIAdem Decision Engine"}

@app.post("/decision")
def decision(location: str, food: str, money: str, risk: str):

    result = generate_choices(location, food, money, risk)

    return {
        "location": location,
        "choices": result
    }
