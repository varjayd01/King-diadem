# ENGINE/engine_router.py

try:
    from AI.intent_engine import analyze_intent as detect_intent
except Exception:
    detect_intent = None

try:
    from ENGINE.decision_engine import DecisionEngine
    _engine = DecisionEngine()
except Exception:
    _engine = None

try:
    from AI.freedom_signal import freedom_index
except Exception:
    freedom_index = lambda: 0

def run_system(user_input: str) -> dict:
    intent = detect_intent(user_input) if detect_intent else {"intent": "general", "confidence": 0.5}

    if _engine:
        decision = _engine.run({"input": user_input})
    else:
        decision = {"status": "OFFLINE", "message": "Engine offline"}

    risk = decision.get("risk_score", 0)
    freedom = freedom_index()

    return {
        "intent": intent,
        "decision": decision,
        "risk": risk,
        "freedom": freedom
    }
