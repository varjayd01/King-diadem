from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ENGINE.decision_engine import generate_choices

app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DecisionInput(BaseModel):
    location: str
    food: str
    money: str
    risk: str

@app.get("/")
def root():
    return {"system": "KING DIADEM Decision Engine"}

@app.post("/decision")
def decision(data: DecisionInput):

    result = generate_choices(
        data.location,
        data.food,
        data.money,
        data.risk
    )

    return {
        "location": data.location,
        "choices": result
    }
