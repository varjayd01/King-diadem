import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# =========================
# SAFE IMPORTS
# =========================

try:
    from AI.persona_engine import PersonaEngine
except:
    PersonaEngine=None

try:
    from AI.council_engine import Council
except:
    Council=None

try:
    from AI.simulation_engine import Simulation
except:
    Simulation=None

try:
    from AI.world_connector import WorldConnector
except:
    WorldConnector=None

try:
    from SECURITY.emergency_mode import check_emergency
except:
    def check_emergency(ip): return True

try:
    from SECURITY.survival_mode import survival_check
except:
    def survival_check(): return "ok"

try:
    from AI_KERNEL.living_water import detect_leak
except:
    def detect_leak(t): return False

try:
    from AI_KERNEL.scl7_core import enforce_scl7
except:
    def enforce_scl7(): return {}

try:
    from AI.decision_memory import save_decision,get_memory
except:
    def save_decision(q,r): pass
    def get_memory(): return []

try:
    from NETWORK.global_network import add_message,get_messages
except:
    chat=[]
    def add_message(u,m):
        chat.append({"user":u,"message":m})
    def get_messages():
        return chat


# =========================
# INIT SYSTEMS
# =========================

persona = PersonaEngine() if PersonaEngine else None
council = Council() if Council else None
simulation = Simulation() if Simulation else None
world = WorldConnector() if WorldConnector else None


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# =========================
# SYSTEM HEALTH
# =========================

@app.get("/system/health")
async def system_health():

    return {

        "system":"KING DIADEM",

        "modules":[

            "persona_engine",

            "ai_council",

            "simulation_engine",

            "decision_memory",

            "global_network",

            "security",

            "ai_kernel"

        ],

        "status":"running"

    }


# =========================
# AI ASK
# =========================

@app.post("/ask")

async def ask(request:Request):

    body = await request.json()

    question = body.get("question","")

    ip = request.client.host

    if not check_emergency(ip):

        return {"error":"Emergency request limit reached"}

    if survival_check()=="throttle":

        return {"error":"Server busy"}

    leak = detect_leak(question)

    intent="general"

    if persona:

        intent = persona.detect_intent(question)

    opinions={}

    if council:

        opinions = council.deliberate(question)

    paths=[]

    if simulation:

        paths = simulation.simulate(question)

    world_data={}

    if world:

        world_data = world.world_status()

    kernel = enforce_scl7()

    save_decision(question,paths)

    return {

        "question":question,

        "intent":intent,

        "leak_detected":leak,

        "council":opinions,

        "simulation":paths,

        "world":world_data,

        "kernel":kernel

    }


# =========================
# DECISION MAP
# =========================

@app.post("/decision")

async def decision(request:Request):

    body = await request.json()

    q = body.get("question","")

    if simulation:

        options = simulation.simulate(q)

    else:

        options=["advance","wait","pivot"]

    return {

        "problem":q,

        "options":options

    }


# =========================
# GLOBAL CHAT
# =========================

@app.post("/world/chat")

async def world_chat(request:Request):

    body=await request.json()

    user=body.get("user","anon")

    msg=body.get("message","")

    add_message(user,msg)

    return {"status":"ok"}


@app.get("/world/messages")

async def world_messages():

    return get_messages()


# =========================
# MEMORY
# =========================

@app.get("/memory")

async def memory():

    return get_memory()


# =========================
# ROOT
# =========================

@app.get("/")

async def root():

    return {"KING DIADEM":"AI Strategic Command Center"}


# =========================
# RUN
# =========================

if __name__ == "__main__":

    port=int(os.environ.get("PORT",10000))

    uvicorn.run(

        "server:app",

        host="0.0.0.0",

        port=port

    )
