from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import time
from collections import defaultdict

from ENGINE.decision_engine import run_decision
from AI.intent_engine import detect_intent
from AI.persona_engine import build_persona

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

GUEST_LIMIT = 5
guest_requests = defaultdict(list)

def check_guest(ip):

    now = time.time()

    guest_requests[ip] = [
        t for t in guest_requests[ip]
        if now - t < 86400
    ]

    if len(guest_requests[ip]) >= GUEST_LIMIT:
        return False

    guest_requests[ip].append(now)
    return True


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/system/health")
def health():

    return {
        "server":"online",
        "ai":"active",
        "wallet":"ready"
    }


@app.post("/decision")
async def decision(req:Request):

    ip = req.client.host

    if not check_guest(ip):

        return {
            "error":"guest limit reached"
        }

    data = await req.json()

    text = data["problem"]

    intent = detect_intent(text)

    persona = build_persona(intent)

    result = run_decision(text, persona)

    return result


@app.get("/ai/brain")
def brain():

    return {

        "modules":[
            "intent_engine",
            "persona_engine",
            "decision_engine",
            "simulation_engine"
        ]

    }


@app.get("/ai/galaxy")
def galaxy():

    return {

        "nodes":[

            {"name":"AI CORE"},
            {"name":"DECISION ENGINE"},
            {"name":"SIMULATION"},
            {"name":"PERSONA SYSTEM"},
            {"name":"GLOBAL NODE"}

        ]

    }
