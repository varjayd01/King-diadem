from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json, os, uuid, hashlib

from ENGINE.decision_engine import KingDiademEngine

app = FastAPI()
engine = KingDiademEngine()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")


# DB
FILE="data/users.json"

def load():
    if not os.path.exists(FILE): return {}
    return json.load(open(FILE))

def save(d):
    os.makedirs("data",exist_ok=True)
    json.dump(d,open(FILE,"w"),indent=2)

def hash(p): return hashlib.sha256(p.encode()).hexdigest()

def find(k,d):
    for e in d:
        if d[e]["api_key"]==k:
            return e


# schema
class Req(BaseModel):
    api_key:str
    question:str
    mode:str="chat"


@app.post("/signup")
def signup(r:Req):
    d=load()
    k="kd_"+uuid.uuid4().hex
    d[str(len(d))]={"password":"x","credits":10,"api_key":k}
    save(d)
    return {"api_key":k}


@app.post("/decision")
def decision(r:Req):

    d=load()
    u=find(r.api_key,d)

    if not u:
        raise HTTPException(401)

    if d[u]["credits"]<=0:
        return {"reply":"หมด"}

    d[u]["credits"]-=1
    save(d)

    return engine.run(r.question, r.mode)
