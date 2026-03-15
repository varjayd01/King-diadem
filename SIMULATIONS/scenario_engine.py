import random
import time


def simulate_future(context):

    if not isinstance(context, dict):

        return {
            "error": "invalid context"
        }

    # ตัวแปรพื้นฐาน
    risk = random.uniform(0.1, 0.9)
    success = random.uniform(0.3, 0.95)

    outlook = "stable"

    if success > 0.75:
        outlook = "growth"

    elif success < 0.45:
        outlook = "decline"

    result = {

        "timestamp": time.time(),

        "input": context,

        "future_projection": {

            "success_probability": round(success, 3),

            "risk_level": round(risk, 3),

            "outlook": outlook
        }
    }

    return result
