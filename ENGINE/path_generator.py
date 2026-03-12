def generate_paths(state):

    paths = []

    if state["dependency"]:
        paths.append("start_small_income")

    if state["depression"]:
        paths.append("mental_support")

    if state["violence_risk"]:
        paths.append("safe_exit_plan")

    paths.append("restore_personal_choice")

    return paths
