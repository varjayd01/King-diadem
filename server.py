import os
import uvicorn

from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles

from AI.decision_engine import process_decision
from AI.freedom_signal import freedom_index
from AI.global_decision_map import decision_map
from AI.galaxy_visualization import galaxy_nodes

from NETWORK.global_chat import add_chat,get_chat
from NETWORK.node_registry import register_node,get_nodes


app=FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")


@app.get("/",response_class=HTMLResponse)
async def root():

    with open("static/index.html","r",encoding="utf-8") as f:

        return f.read()


@app.post("/ask")
async def ask(request:Request):

    data=await request.json()

    question=data.get("question","")

    options=process_decision(question)

    return JSONResponse({

        "question":question,
        "options":options

    })


@app.get("/freedom")
def freedom():

    score=freedom_index()

    status="stable"

    if score<30:

        status="compression"

    if score>60:

        status="expansion"

    return{

        "freedom_index":score,
        "status":status

    }


@app.get("/decision/map")
def map():

    return{

        "nodes":decision_map()

    }


@app.get("/galaxy")
def galaxy():

    return{

        "stars":galaxy_nodes()

    }


@app.post("/world/chat")
async def world_chat(request:Request):

    data=await request.json()

    user=data.get("user","anonymous")

    message=data.get("message","")

    add_chat(user,message)

    return{

        "status":"ok"

    }


@app.get("/world/messages")
def messages():

    return{

        "messages":get_chat()

    }


@app.post("/network/register")
async def register(request:Request):

    data=await request.json()

    node_id=data.get("node_id")

    location=data.get("location","unknown")

    register_node(node_id,location)

    return{

        "status":"registered"

    }


@app.get("/network/nodes")
def nodes():

    return{

        "nodes":get_nodes()

    }


if __name__=="__main__":

    port=int(os.environ.get("PORT",10000))

    uvicorn.run(app,host="0.0.0.0",port=port)
