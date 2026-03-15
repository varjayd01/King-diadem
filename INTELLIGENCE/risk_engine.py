import math

from SIMULATIONS.entropy_engine import analyze_entropy
from SIMULATIONS.montecarlo_engine import run_montecarlo
from SIMULATIONS.black_swan_detector import detect_black_swan


def clamp(x, min_v=0.0, max_v=1.0):
    return max(min_v, min(max_v, x))


def volatility(max_score, min_score):

    spread = max_score - min_score

    return clamp(spread)


def downside_asymmetry(avg, min_score):

    downside = avg - min_score

    if downside <= 0:
        return 0

    return clamp(downside * 1.5)


def fragility_index(vol, tail):

    fragility = (vol * 0.6) + (tail * 0.4)

    return clamp(fragility)


def entropy_risk(entropy_state):

    mapping = {

        "high stability": 0.1,
        "balanced": 0.3,
        "unstable": 0.65,
        "collapse risk": 0.95
    }

    return mapping.get(entropy_state, 0.5)


def classify_risk(score):

    if score < 0.20:
        return "low"

    elif score < 0.40:
        return "moderate"

    elif score < 0.60:
        return "high"

    elif score < 0.80:
        return "severe"

    return "critical"


def antifragile_signal(avg, vol):

    if avg > 0.4 and vol > 0.5:
        return True

    return False


def decision_pressure(risk_score, volatility):

    pressure = (risk_score * 0.7) + (volatility * 0.3)

    return clamp(pressure)


def analyze_risk(base_score):

    # ---------- ENTROPY ----------

    entropy = analyze_entropy({

        "entropy": 50,
        "stability": base_score * 100
    })

    entropy_score = entropy_risk(entropy["system_state"])


    # ---------- MONTE CARLO ----------

    monte = run_montecarlo(base_score)

    avg = monte["average_score"]
    min_s = monte["min"]
    max_s = monte["max"]


    vol = volatility(max_s, min_s)

    tail = downside_asymmetry(avg, min_s)


    fragility = fragility_index(vol, tail)


    # ---------- BLACK SWAN ----------

    swan = detect_black_swan()

    swan_penalty = 0.0

    if swan["black_swan"]:
        swan_penalty = 0.45


    # ---------- COMBINED RISK MODEL ----------

    risk_score = (

        entropy_score * 0.30 +
        vol * 0.20 +
        tail * 0.25 +
        fragility * 0.15 +
        swan_penalty * 0.10

    )

    risk_score = clamp(risk_score)


    risk_level = classify_risk(risk_score)


    # ---------- STABILITY INDEX ----------

    stability_index = clamp(

        (avg + 1) / 2 - risk_score
    )


    # ---------- ANTIFRAGILE ----------

    antifragile = antifragile_signal(avg, vol)


    # ---------- DECISION PRESSURE ----------

    pressure = decision_pressure(risk_score, vol)


    return {

        "risk_score": round(risk_score, 3),

        "risk_level": risk_level,

        "stability_index": round(stability_index, 3),

        "fragility_index": round(fragility, 3),

        "decision_pressure": round(pressure, 3),

        "entropy_state": entropy["system_state"],

        "volatility": round(vol, 3),

        "tail_risk": round(tail, 3),

        "montecarlo_range": [min_s, max_s],

        "black_swan_detected": swan["black_swan"],

        "antifragile_system": antifragile
    }
