# ENGINE/engine_router.py

from AI.intent_engine import detect_intent
from ENGINE.decision_engine import make_decision
from ENGINE.simulation_engine import simulate
from ENGINE.risk_engine import evaluate_risk
from AI.freedom_signal import freedom_index

def run_system(user_input):

    # 1. เข้าใจเจตนา
    intent = detect_intent(user_input)

    # 2. ประมวลผลการตัดสินใจ
    decision = make_decision(user_input, intent)

    # 3. จำลองผลลัพธ์
    sim = simulate(decision)

    # 4. ประเมินความเสี่ยง
    risk = evaluate_risk(sim)

    # 5. วัด freedom
    freedom = freedom_index()

    return {
        "intent": intent,
        "decision": decision,
        "simulation": sim,
        "risk": risk,
        "freedom": freedom
    }
