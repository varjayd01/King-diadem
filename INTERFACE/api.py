from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ENGINE.decision_engine import generate_choices

app = FastAPI()

# --- CORS FIX ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"system": "KING DIADEM Decision Engine"}

@app.post("/decision")
def decision(location: str, food: str, money: str, risk: str):

    result = generate_choices(location, food, money, risk)

    return {
        "location": location,
        "choices": result
    }
