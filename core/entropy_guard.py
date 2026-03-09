# Entropy Guard
# Drift detection system

def entropy_check(system_state):

    entropy = system_state.get("entropy",50)
    stability = system_state.get("stability",50)

    if entropy > 80:

        return {
            "status":"critical_entropy",
            "action":"stabilize_system"
        }

    if entropy > 60:

        return {
            "status":"entropy_rising",
            "action":"increase_vigilance"
        }

    if stability < 40:

        return {
            "status":"low_stability",
            "action":"reduce_system_load"
        }

    return {
        "status":"stable",
        "action":"observe"
  }
