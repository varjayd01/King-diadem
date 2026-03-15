import time

from INTELLIGENCE.risk_engine import analyze_risk
from INTELLIGENCE.decision_intelligence import intelligence_layer
from DATABASE.decision_history import save_decision


def analyze_business(context):

    revenue = context.get("revenue", 0)
    cost = context.get("cost", 0)

    market_growth = context.get("market_growth", 0.5)
    competition = context.get("competition", 0.5)
    demand = context.get("demand", 0.5)

    profit = revenue - cost

    margin = 0

    if revenue > 0:
        margin = profit / revenue


    # ---------- OPPORTUNITY MODEL ----------

    opportunity_score = (

        market_growth * 0.35 +
        demand * 0.40 +
        (1 - competition) * 0.25

    )


    # ---------- COST PRESSURE ----------

    cost_pressure = 0

    if revenue > 0:
        cost_pressure = cost / revenue


    # ---------- CORE BUSINESS SCORE ----------

    base_score = (

        opportunity_score * 0.6 +
        margin * 0.4

    )


    # ---------- RISK ANALYSIS ----------

    risk = analyze_risk(base_score)


    # ---------- STRATEGY ENGINE ----------

    strategy = "observe"


    if margin < 0:
        strategy = "pivot"

    elif risk["risk_level"] == "critical":
        strategy = "defensive"

    elif opportunity_score > 0.75 and margin > 0.25:
        strategy = "scale"

    elif opportunity_score > 0.55:
        strategy = "optimize"

    elif demand < 0.3:
        strategy = "rethink_market"


    # ---------- RESULT OBJECT ----------

    result = {

        "domain": "business",

        "timestamp": time.time(),

        "input": context,

        "profit": profit,

        "profit_margin": round(margin, 3),

        "opportunity_score": round(opportunity_score, 3),

        "cost_pressure": round(cost_pressure, 3),

        "base_score": round(base_score, 3),

        "recommended_strategy": strategy,

        "risk_analysis": risk

    }


    # ---------- SAVE DECISION HISTORY ----------

    save_decision(result)


    # ---------- INTELLIGENCE LAYER ----------

    return intelligence_layer(result)
