def run_decision(data):

    if not isinstance(data, dict):

        return {
            "result": "invalid input",
            "advice": "send JSON object"
        }

    if len(data) == 0:

        return {
            "result": "no data",
            "advice": "provide decision context"
        }

    # ตัวอย่าง logic

    decision = {
        "analysis": data,
        "recommendation": "optimize",
        "confidence": 0.65
    }

    return decision
