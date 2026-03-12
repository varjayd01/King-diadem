# KING DIADEM Collapse Predictor

def predict_collapse(risk_score):

    if risk_score > 80:
        return "high collapse probability"

    if risk_score > 60:
        return "moderate collapse probability"

    return "low collapse probability"
