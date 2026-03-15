import time


def analyze_business(context):

    revenue = context.get("revenue", 0)
    cost = context.get("cost", 0)

    market_growth = context.get("market_growth", 0.5)
    demand = context.get("demand", 0.5)

    competition = context.get("competition", 0.5)
    barrier = context.get("barrier_to_entry", 0.5)

    runway = context.get("runway_months", 12)

    # ---------- FINANCIAL ----------

    profit = revenue - cost

    margin = 0
    if revenue > 0:
        margin = profit / revenue

    burn_risk = 0
    if runway < 12:
        burn_risk = (12 - runway) / 12

    financial_strength = (
        margin * 0.6 +
        (1 - burn_risk) * 0.4
    )

    # ---------- MARKET ----------

    market_power = (
        market_growth * 0.4 +
        demand * 0.4 +
        barrier * 0.2
    )

    # ---------- COMPETITION ----------

    competitive_pressure = (
        competition * 0.7 +
        (1 - barrier) * 0.3
    )

    # ---------- SURVIVAL ----------

    survival_resilience = (
        runway / 24
    )

    if survival_resilience > 1:
        survival_resilience = 1

    # ---------- STRATEGIC SCORE ----------

    strategic_score = (
        financial_strength * 0.35 +
        market_power * 0.30 +
        survival_resilience * 0.20 -
        competitive_pressure * 0.25
    )

    # ---------- STRATEGY ----------

    strategy = "observe"

    if strategic_score > 0.6:
        strategy = "scale aggressively"

    elif strategic_score > 0.45:
        strategy = "controlled expansion"

    elif strategic_score > 0.25:
        strategy = "optimize operations"

    elif strategic_score > 0:
        strategy = "defensive strategy"

    else:
        strategy = "pivot or restructure"

    return {

        "domain": "business",

        "timestamp": time.time(),

        "input": context,

        "profit": profit,

        "profit_margin": round(margin,3),

        "financial_strength": round(financial_strength,3),

        "market_power": round(market_power,3),

        "competitive_pressure": round(competitive_pressure,3),

        "survival_resilience": round(survival_resilience,3),

        "strategic_score": round(strategic_score,3),

        "recommended_strategy": strategy
    }
