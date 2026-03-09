# Drift Monitor
# Detect structural drift before collapse

def detect_drift(system_state):

    entropy = system_state.get("entropy", 50)
    stability = system_state.get("stability", 50)

    drift_score = entropy - stability

    if drift_score > 30:

        return {
            "status": "critical_drift",
            "action": "stabilize_system"
        }

    if drift_score > 10:

        return {
            "status": "early_warning",
            "action": "increase_vigilance"
        }

    return {
        "status": "stable",
        "action": "observe"
    }
