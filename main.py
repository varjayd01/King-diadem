from fastapi import FastAPI, HTTPException, Security
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json, os, uuid

# Import logic core จากที่พี่วางโครงไว้
from ENGINE.decision_engine import KingDiademEngine

app = FastAPI(title="KING DIADEM OS")
engine = KingDiademEngine() # Singleton Engine

# Setup Path
DATA_DIR = "data"
USER_FILE = os.path.join(DATA_DIR, "users.json")
os.makedirs(DATA_DIR, exist_ok=True)

# --- HELPER FUNCTIONS ---
def get_db():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def commit_db(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --- SCHEMA ---
class ActionReq(BaseModel):
    api_key: str
    question: str
    mode: str = "chat"

# --- ROUTES ---
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")

@app.post("/signup")
def signup():
    db = get_db()
    new_id = str(uuid.uuid4())[:8] # Short UUID for ID
    api_key = f"kd_{uuid.uuid4().hex}"
    
    db[new_id] = {
        "api_key": api_key,
        "credits": 10,
        "status": "active"
    }
    commit_db(db)
    return {"api_key": api_key, "msg": "Welcome to the Kernel"}

@app.post("/decision")
def run_decision(r: ActionReq):
    db = get_db()
    
    # 1. Identity Check (Identity Radius)
    user_entry = next((uid for uid, info in db.items() if info.get("api_key") == r.api_key), None)
    
    if not user_entry:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2. Resource Check (Energy Conservation)
    if db[user_entry]["credits"] <= 0:
        raise HTTPException(status_code=402, detail="Energy Depleted: Credits = 0")

    # 3. Execution (LYLA/VEGA Mode)
    try:
        reply = engine.run(r.question, r.mode)
        
        # 4. Update State (Post-Action)
        db[user_entry]["credits"] -= 1
        commit_db(db)
        
        return reply
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
