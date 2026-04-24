from fastapi import FastAPI
from pydantic import BaseModel
from ENGINE.decision_engine import DecisionEngine

app = FastAPI()
engine = DecisionEngine()

class InputData(BaseModel):
    input: str
    state: dict = {}

@app.post("/run")
def run(data: InputData):
    return engine.run(data.dict())
