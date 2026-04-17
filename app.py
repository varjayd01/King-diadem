# app.py

import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from ENGINE.universal_engine import run_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="KING DIADEM")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


class InputData(BaseModel):
    input: str = Field(default="")
    entropy: float = Field(default=40)
    resource: float = Field(default=50)
    stability: float = Field(default=60)
    choices: int = Field(default=1)
    confidence: float = Field(default=0.5)


@app.get("/")
def root():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ENGINE")
def engine(data: InputData):
    return run_engine(data.model_dump())
