from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ENGINE.decision_engine import decision_engine

app = FastAPI()


# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- INPUT MODEL ----
class DecisionInput(BaseModel):
    location: str
    food: str
    money: str
    risk: str


# ---- HOMEPAGE ----
@app.get("/", response_class=HTMLResponse)
async def homepage():

    with open("INTERFACE/index.html") as f:
        return f.read()


# ---- SYSTEM CHECK ----
@app.get("/system")
def system():
    return {"system": "KING DIADEM Decision Engine"}


# ---- DECISION ENGINE API ----
@app.post("/decision")
def decision(data: DecisionInput):

    result = decision_engine(
        data.location,
        data.food,
        data.money,
        data.risk
    )

    return result
