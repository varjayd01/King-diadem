def predict_collapse(state):

    score = 0

    if state["depression"]:
        score += 25

    if state["dependency"]:
        score += 40

    if state["violence_risk"]:
        score += 80

    return min(score,100)
