# Drift Monitor

def detect_drift(system_state):

    entropy = system_state.get("entropy",50)
    stability = system_state.get("stability",50)

    drift_score = entropy - stability

    if drift_score > 30:

        return "system_drift_detected"

    if drift_score > 10:

        return "early_drift_warning"

    return "stable"
