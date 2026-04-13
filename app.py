from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from brain import run_brain

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")


class ChatInput(BaseModel):
    message: str


@app.post("/chat")
def chat(data: ChatInput):

    if not data.message:
        return {"reply": "..."}

    reply = run_brain(data.message)

    return {"reply": reply}
