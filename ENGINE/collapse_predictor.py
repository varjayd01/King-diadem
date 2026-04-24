# =========================
# ⚠️ KING DIADEM
# Collapse Predictor (Upgraded)
# =========================

def _clamp(x, low=0, high=100):
    try:
        x = float(x)
    except:
        x = 0
    return max(low, min(high, x))


# =========================
# 🧠 CORE PREDICTOR
# =========================
def predict_collapse(risk_score):

    risk_score = _clamp(risk_score)

    if risk_score >= 85:
        level = "CRITICAL"
        probability = 0.9

    elif risk_score >= 65:
        level = "HIGH"
        probability = 0.7

    elif risk_score >= 40:
        level = "MEDIUM"
        probability = 0.4

    else:
        level = "LOW"
        probability = 0.1

    return {
        "risk_score": risk_score,
        "collapse_level": level,
        "probability": probability,
        "prediction": _text(level)
    }


def _text(level):
    mapping = {
        "CRITICAL": "Collapse imminent",
        "HIGH": "High collapse probability",
        "MEDIUM": "Moderate instability",
        "LOW": "System stable"
    }
    return mapping.get(level, "Unknown")


# =========================
# 🔥 ADAPTER (ให้ DecisionEngine เรียกได้)
# =========================
def analyze(pattern: dict):

    try:
        risk = float(pattern.get("entropy", 40))  # fallback

        # ถ้ามี risk_engine ส่งมา
        if "risk_score" in pattern:
            risk = pattern["risk_score"]

        return predict_collapse(risk)

    except Exception as e:
        return {"error": f"collapse_predictor fail: {str(e)}"}
