from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ENGINE.decision_engine import decision_engine

app = FastAPI(
    title="KING DIADEM",
    docs_url="/docs"
)


# -------------------
# CORS
# -------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------
# INPUT MODEL
# -------------------

class DecisionInput(BaseModel):
    location: str
    food: str
    money: int
    risk: str


# -------------------
# HOMEPAGE
# -------------------

@app.get("/", response_class=HTMLResponse)
async def homepage():

    with open("INTERFACE/index.html") as f:
        return f.read()


# -------------------
# SYSTEM STATUS
# -------------------

@app.get("/system")
def system():

    return {
        "system": "KING DIADEM",
        "status": "online"
    }


# -------------------
# DECISION ENGINE
# -------------------

@app.post("/decision")
def decision(data: DecisionInput):

    result = decision_engine(
        data.location,
        data.food,
        data.money,
        data.risk
    )

    return result
@app.post("/mobile/node")

def mobile_node(data: dict):

    location = data.get("location")
    food = data.get("food")
    risk = data.get("risk")

    world = mobile_report(location, food, risk)

    return {
        "status": "node registered",
        "world": world
    }
