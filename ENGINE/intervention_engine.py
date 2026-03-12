# KING DIADEM Intervention Engine

def intervention(risk_state):

    if risk_state == "critical":
        return "immediate relocation"

    if risk_state == "unstable":
        return "stabilize resources"

    return "maintain current strategy"
