def run_decision(body):

    if not body:
        return "No input provided"

    if isinstance(body, dict):

        problem = body.get("problem")

        if problem:

            return {
                "analysis": f"Analyzing: {problem}",
                "strategy": "Optimize resource allocation",
                "risk": "Unknown variables present"
            }

    return {
        "analysis": "Generic decision",
        "strategy": "Gather more data",
        "risk": "Low"
    }
