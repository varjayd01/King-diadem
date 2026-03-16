import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# =============================
# IMPORT AI SYSTEMS
# =============================

from AI.persona_engine import PersonaEngine
from AI.council_engine import Council
from AI.simulation_engine import Simulation
from AI.world_connector import WorldConnector

from SECURITY.emergency_mode import check_emergency
from SECURITY.survival_mode import survival_check

from AI_KERNEL.living_water import detect_leak
from AI_KERNEL.scl7_core import enforce_scl7


# =============================
# INIT SYSTEMS
# =============================

persona = PersonaEngine()
council = Council()
simulation = Simulation()
world = WorldConnector()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# STATIC FILES
# =============================

app.mount("/static", StaticFiles(directory="static"), name="static")


# =============================
# HEALTH CHECK
# =============================

@app.get("/system/health")
async def health():

    return {
        "system":"KING DIADEM",
        "status":"running",
        "modules":[
            "persona",
            "council",
            "simulation",
            "world_connector",
            "security",
            "ai_kernel"
        ]
    }


# =============================
# MAIN AI ENDPOINT
# =============================

@app.post("/ask")
async def ask(request: Request):

    body = await request.json()
    question = body.get("question","")

    ip = request.client.host

    # emergency mode
    if not check_emergency(ip):

        return JSONResponse({
            "error":"Emergency limit reached (5 requests/hour)"
        })

    # server survival
    if survival_check() == "throttle":

        return JSONResponse({
            "error":"Server busy, please wait"
        })

    # living water detection
    leak = detect_leak(question)

    # intent detection
    intent = persona.detect_intent(question)

    # council meeting
    opinions = council.deliberate(question)

    # simulation
    paths = simulation.simulate(question)

    # world data
    world_data = world.world_status()

    # kernel rules
    rules = enforce_scl7()

    return {

        "question":question,

        "intent":intent,

        "leak_detected":leak,

        "council":opinions,

        "simulation":paths,

        "world":world_data,

        "kernel_rules":rules

    }


# =============================
# DECISION MAP
# =============================

@app.post("/decision")
async def decision(request: Request):

    body = await request.json()
    question = body.get("question","")

    paths = simulation.simulate(question)

    return {

        "problem":question,

        "options":paths

    }


# =============================
# ROOT
# =============================

@app.get("/")
async def root():

    return JSONResponse({
        "message":"KING DIADEM AI Strategic Command Center"
    })


# =============================
# RUN
# =============================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
