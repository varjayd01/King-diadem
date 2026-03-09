from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ENGINE.decision_engine import decision_engine

app = FastAPI(
    title="KING DIADEM",
    docs_url="/docs"
)

# CORS
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


# หน้าเว็บหลัก
@app.get("/", response_class=HTMLResponse)
async def homepage():
    with open("INTERFACE/index.html") as f:
        return f.read()


# API ตัดสินใจ
@app.post("/decision")
def decision(data: DecisionInput):

    result = decision_engine(
        data.location,
        data.food,
        data.money,
        data.risk
    )

    return result


# เช็คระบบ
@app.get("/system")
def system():
    return {"system": "KING DIADEM Decision Engine"}
