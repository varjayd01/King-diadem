from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI
import os

from ENGINE.decision_engine import run_decision

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app.mount("/static", StaticFiles(directory="static"), name="static")

class InputData(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
def index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/run")
def run(data: InputData):

    decision = run_decision(data.text)

    try:
        res = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": data.text}
            ]
        )
        ai = res.choices[0].message.content

    except Exception as e:
        ai = f"[GPT FAIL] {str(e)}"

    return {
        "decision": decision,
        "ai": ai
    }
