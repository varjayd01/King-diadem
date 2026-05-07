"""
KING DIADEM - Main Application
Connects: AI (Gemini) + Decision Engine + Frontend + Database
"""

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import sys
from typing import Optional, Dict, Any, List

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import core systems
from core.llm_gemini_final import GeminiAI
from ENGINE.decision_core import DecisionCore

# ============================================
# APP INITIALIZATION
# ============================================

app = FastAPI(
    title="KING DIADEM",
    description="Decision Intelligence System - Stable Before Great",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# REQUEST MODELS
# ============================================

class DecisionRequest(BaseModel):
    """Request for decision analysis"""
    situation: str
    resources: Optional[Dict[str, Any]] = {}
    constraints: Optional[Dict[str, Any]] = {}
    urgency: Optional[str] = "medium"

class ChatRequest(BaseModel):
    """Simple chat request"""
    message: str
    user_id: Optional[str] = None

# ============================================
# CORE SYSTEM - Master Brain
# ============================================

class MasterBrain:
    """
    Master orchestrator for KING DIADEM
    Combines: Gemini AI + Decision Engine + Memory
    """
    
    def __init__(self):
        self.ai = None
        self.decision_engine = None
        self.ready = False
        self.initialize()
    
    def initialize(self):
        """Initialize all systems"""
        print("\n" + "="*60)
        print("KING DIADEM SYSTEM INITIALIZING")
        print("="*60)
        
        # 1. Initialize Gemini AI
        try:
            self.ai = GeminiAI()
            if self.ai.is_ready():
                print("✓ Gemini AI: READY")
            else:
                print("⚠ Gemini AI: NOT CONFIGURED (set GEMINI_API_KEY)")
        except Exception as e:
            print(f"✗ Gemini AI: FAILED - {e}")
        
        # 2. Initialize Decision Engine
        try:
            self.decision_engine = DecisionCore()
            print("✓ Decision Engine: READY")
        except Exception as e:
            print(f"✗ Decision Engine: FAILED - {e}")
        
        self.ready = True
        print("="*60)
        print("STATUS: OPERATIONAL")
        print("="*60 + "\n")
    
    async def process_decision(self, request: DecisionRequest) -> Dict:
        """Main decision processing pipeline"""
        
        # Build context
        context = {
            "situation": request.situation,
            "resources": request.resources,
            "constraints": request.constraints,
            "urgency": request.urgency
        }
        
        # Step 1: Generate base choices (Decision Engine)
        base_choices = self.decision_engine.generate_choices(context)
        
        # Step 2: AI Analysis (if available)
        ai_analysis = None
        if self.ai and self.ai.is_ready():
            ai_analysis = await self.ai.analyze_situation(context)
        
        # Step 3: Combine results
        result = {
            "status": "success",
            "situation": request.situation,
            "urgency": self.decision_engine.evaluate_urgency(context),
            "choices": base_choices,
            "ai_insights": ai_analysis,
            "metadata": {
                "choice_count": len(base_choices),
                "ai_available": self.ai is not None and self.ai.is_ready()
            }
        }
        
        return result
    
    async def chat(self, message: str) -> str:
        """Simple chat interface"""
        
        if self.ai and self.ai.is_ready():
            response = await self.ai.ask(message)
            return response
        else:
            return "AI ไม่พร้อมใช้งาน - กรุณาตั้งค่า GEMINI_API_KEY"

# Initialize Master Brain
brain = MasterBrain()

# ============================================
# API ENDPOINTS
# ============================================

@app.get("/")
async def root():
    """Serve main page"""
    return FileResponse("static/index.html")

@app.get("/health")
async def health():
    """System health check"""
    return {
        "status": "operational",
        "systems": {
            "ai": brain.ai.is_ready() if brain.ai else False,
            "decision_engine": brain.decision_engine is not None,
            "ready": brain.ready
        },
        "version": "1.0.0"
    }

@app.post("/api/decision")
async def make_decision(request: DecisionRequest):
    """Generate decision choices"""
    try:
        result = await brain.process_decision(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat with AI"""
    try:
        response = await brain.chat(request.message)
        return {
            "response": response,
            "ai_available": brain.ai.is_ready() if brain.ai else False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
async def analyze(request: DecisionRequest):
    """Quick analysis endpoint"""
    try:
        if not brain.ai or not brain.ai.is_ready():
            raise HTTPException(
                status_code=503, 
                detail="AI not available - configure GEMINI_API_KEY"
            )
        
        analysis = await brain.ai.analyze_situation({
            "situation": request.situation,
            "resources": request.resources
        })
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket for real-time
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time decision stream"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Process decision
            request = DecisionRequest(**data)
            result = await brain.process_decision(request)
            
            await websocket.send_json(result)
    
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    print("⚠ Warning: static directory not found")

# ============================================
# STARTUP
# ============================================

@app.on_event("startup")
async def startup():
    """Run on startup"""
    print("\n🚀 KING DIADEM is running")
    print(f"📍 Open: http://localhost:8000")
    print(f"📊 Health: http://localhost:8000/health")
    print(f"📖 Docs: http://localhost:8000/docs\n")

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
