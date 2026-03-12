def intervention(paths):

    advice = []

    if "safe_exit_plan" in paths:
        advice.append("prepare safe location and trusted contact")

    if "start_small_income" in paths:
        advice.append("build independent income source")

    if "mental_support" in paths:
        advice.append("seek emotional support network")

    return advice
