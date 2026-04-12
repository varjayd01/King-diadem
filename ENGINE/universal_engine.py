# UNIVERSAL ENGINE (รวมทุกระบบของพี่)

from ENGINE.decision_engine import run_decision
from DOMAINS.domain_router import route_domain

def UNIVERSAL_ENGINE(input_data: dict):
    """
    input_data = {
        location, food, money, risk
    }
    """

    try:
        # 1. route domain
        domain = route_domain(input_data)

        # 2. decision core
        decision = run_decision(input_data)

        # 3. final output format (สำคัญมาก)
        return {
            "status": "ok",
            "domain": domain,
            "decision": decision
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
