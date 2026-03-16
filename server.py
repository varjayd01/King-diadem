import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# ===== AI CORE =====

from AI.persona_engine import PersonaEngine
from AI.council_engine import Council
from AI.simulation_engine import Simulation
from AI.world_connector import WorldConnector

# ===== KERNEL =====

from AI_KERNEL.cosmic_latte import cosmic_reference
from AI_KERNEL.scl7_core import enforce_scl7
from AI_KERNEL.living_water import detect_leak

# ===== SECURITY =====

from SECURITY.emergency_mode import check_emergency
from SERVER.survival_mode import survival_check

# ===== INIT =====

app = FastAPI(title="KING DIADEM")

persona = PersonaEngine()
council = Council()
simulation = Simulation()
world = WorldConnector()

# ===== STATIC =====

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


# ===== HOME =====

@app.get("/", response_class=HTMLResponse)
async def home():

    path = "static/index.html"

    if os.path.exists(path):

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    return "<h1>KING DIADEM</h1>"


# ===== SYSTEM STATUS =====

@app.get("/system/health")
async def health():

    return {

        "system": "KING DIADEM",

        "cosmic_axes": cosmic_reference(),

        "scl7": enforce_scl7(),

        "status": "running"

    }


# ===== DECISION CORE =====

@app.post("/decision")
async def decision(request: Request):

    ip = request.client.host

    # emergency mode

    if not check_emergency(ip):

        raise HTTPException(status_code=429, detail="Emergency limit reached")

    # survival mode

    if survival_check() == "throttle":

        raise HTTPException(status_code=503, detail="Server busy")

    try:

        body = await request.json()

    except:

        body = {}

    question = body.get("question", "")

    # ===== Living Water =====

    leak = detect_leak(question)

    # ===== Persona =====

    intent = persona.detect_intent(question)

    style = persona.detect_style(question)

    # ===== Council =====

    council_result = council.deliberate(question)

    consensus = council.consensus(council_result)

    # ===== Simulation =====

    futures = simulation.simulate(question)

    # ===== World =====

    world_state = world.world_status()

    return {

        "question": question,

        "intent": intent,

        "style": style,

        "living_water_trigger": leak,

        "council": council_result,

        "consensus": consensus,

        "simulation": futures,

        "world": world_state

    }


# ===== SERVER START =====

if __name__ == "__main__":

    uvicorn.run(

        "server:app",

        host="0.0.0.0",

        port=10000

    )
