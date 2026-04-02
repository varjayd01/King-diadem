from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# =========================
# IMPORT ENGINE ของพี่
# =========================
from ENGINE.decision_engine import DecisionEngine
from ENGINE.strategy_planner import StrategyPlanner
from ENGINE.risk_engine import RiskEngine
from ENGINE.resource_estimator import ResourceEstimator
from ENGINE.survival_advisor import SurvivalAdvisor

# fallback ถ้าบางตัวไม่มี
try:
    from ENGINE.dialogue_engine import DialogueEngine
except:
    DialogueEngine = None


# =========================
# INIT SYSTEM
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# LOAD ENGINE
# =========================
decision_engine = DecisionEngine()
strategy_engine = StrategyPlanner()
risk_engine = RiskEngine()
resource_engine = ResourceEstimator()
survival_engine = SurvivalAdvisor()

dialogue_engine = DialogueEngine() if DialogueEngine else None


# =========================
# INPUT MODEL
# =========================
class Input(BaseModel):
    message: str


# =========================
# ROOT CHECK
# =========================
@app.get("/")
def root():
    return {"status": "KING DIADEM ONLINE"}


# =========================
# MAIN BRAIN
# =========================
@app.post("/decision")
def decision(input: Input):

    msg = input.message

    try:
        # 1. วิเคราะห์ความเสี่ยง
        risk = risk_engine.analyze(msg)

        # 2. ประเมินทรัพยากร
        resource = resource_engine.evaluate(msg)

        # 3. วางกลยุทธ์
        strategy = strategy_engine.plan(msg)

        # 4. ตัดสินใจ
        decision = decision_engine.decide(
            message=msg,
            risk=risk,
            resource=resource,
            strategy=strategy
        )

        # 5. survival mode (สำคัญกับพี่)
        survival = survival_engine.guide(msg)

        # 6. response (dialogue)
        if dialogue_engine:
            response = dialogue_engine.respond(
                msg,
                decision=decision,
                strategy=strategy,
                survival=survival
            )
        else:
            response = f"""
DECISION: {decision}
STRATEGY: {strategy}
SURVIVAL: {survival}
"""

        return {
            "response": response,
            "meta": {
                "risk": risk,
                "resource": resource,
                "strategy": strategy
            }
        }

    except Exception as e:
        return {
            "response": "SYSTEM ERROR",
            "error": str(e)
        }
