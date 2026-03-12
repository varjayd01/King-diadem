# KING DIADEM Situation Analyzer

def analyze_situation(food_score, risk_score):

    if risk_score > 70:
        state = "critical"

    elif risk_score > 40:
        state = "unstable"

    else:
        state = "stable"

    if food_score < 30:
        resource_state = "scarcity"
    else:
        resource_state = "sufficient"

    return {
        "risk_state": state,
        "resource_state": resource_state
    }
