# =========================
# KING DIADEM - MAIN APP
# =========================

from fastapi import FastAPI
import traceback

app = FastAPI(title="KING DIADEM", version="1.0")

# =========================
# SAFE IMPORT ZONE
# =========================

engine_status = {
    "engine": False,
    "decision": False,
    "kernel": False
}

try:
    from ENGINE.decision_engine import KingDiademEngine
    engine = KingDiademEngine()
    engine_status["engine"] = True
except Exception as e:
    print("❌ ENGINE LOAD FAIL:", e)
    engine = None

try:
    from decision import make_decision
    engine_status["decision"] = True
except Exception as e:
    print("❌ DECISION LOAD FAIL:", e)
    make_decision = None

try:
    from KING_DIadem_core import KingDiademCore
    core = KingDiademCore()
    engine_status["kernel"] = True
except Exception as e:
    print("❌ CORE LOAD FAIL:", e)
    core = None


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "system": "KING DIADEM",
        "status": "RUNNING",
        "engines": engine_status
    }


# =========================
# DECISION API
# =========================

@app.post("/decision")
def decision_api(data: dict):
    try:
        result = {}

        if make_decision:
            result["decision"] = make_decision(data)

        if engine:
            result["engine"] = engine.process(data)

        if core:
            result["core"] = core.evaluate(data)

        return {
            "status": "ok",
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "trace": traceback.format_exc()
        }


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():
    return {
        "alive": True,
        "engines": engine_status
    }
