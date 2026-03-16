import os
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# AI SYSTEM
from AI.decision_engine import process_decision
from AI.freedom_signal import freedom_index
from AI.global_decision_map import decision_map
from AI.galaxy_visualization import galaxy_nodes
from AI.planetary_reality import planetary_status
from AI.reality_learning import learning_summary

# NETWORK
from NETWORK.global_chat import add_chat, get_chat
from NETWORK.node_registry import register_node, get_nodes


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


# ROOT PAGE
@app.get("/", response_class=HTMLResponse)
async def root():

    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


# ASK DECISION
@app.post("/ask")
async def ask(request: Request):

    data = await request.json()

    question = data.get("question", "")

    options = process_decision(question)

    return JSONResponse({
        "question": question,
        "options": options
    })


# FREEDOM SIGNAL
@app.get("/freedom")
def freedom():

    score = freedom_index()

    status = "stable"

    if score < 30:
        status = "compression"

    if score > 60:
        status = "expansion"

    return {
        "freedom_index": score,
        "status": status
    }


# GLOBAL DECISION MAP
@app.get("/decision/map")
def decision_map_api():

    return {
        "nodes": decision_map()
    }


# GALAXY VISUALIZATION
@app.get("/galaxy")
def galaxy():

    return {
        "stars": galaxy_nodes()
    }


# PLANETARY STATUS
@app.get("/planetary")
def planetary():

    return planetary_status()


# REALITY LEARNING
@app.get("/reality/stats")
def learning():

    return learning_summary()


# GLOBAL CHAT
@app.post("/world/chat")
async def world_chat(request: Request):

    data = await request.json()

    user = data.get("user", "anonymous")

    message = data.get("message", "")

    add_chat(user, message)

    return {"status": "ok"}


@app.get("/world/messages")
def world_messages():

    return {
        "messages": get_chat()
    }


# NETWORK REGISTER
@app.post("/network/register")
async def register(request: Request):

    data = await request.json()

    node_id = data.get("node_id")

    location = data.get("location", "unknown")

    register_node(node_id, location)

    return {"status": "registered"}


# NETWORK NODES
@app.get("/network/nodes")
def nodes():

    return {
        "nodes": get_nodes()
    }


# SERVER START
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    uvicorn.run(app, host="0.0.0.0", port=port)
