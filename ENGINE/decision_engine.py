def decision_intelligence(state, risk):
    score = 100 - risk.get("score", 50)

    if state.get("entropy", 50) > 70:
        action = "STABILIZE"
    elif score > 60:
        action = "PROCEED"
    else:
        action = "WAIT"

    return {
        "action": action,
        "confidence": score / 100,
        "reason": f"entropy={state.get('entropy')} risk={risk.get('score')}"
    }
