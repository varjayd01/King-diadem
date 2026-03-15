import random
import time


def run_decision(data):

    # ป้องกัน input แปลก
    if not isinstance(data, dict):

        return {
            "result": "invalid_input",
            "message": "Input must be JSON object"
        }

    # ถ้าไม่มีข้อมูล
    if len(data) == 0:

        return {
            "result": "no_context",
            "message": "Provide decision context"
        }

    # วิเคราะห์แบบง่ายก่อน
    score = random.uniform(0.4, 0.9)

    recommendation = "proceed"

    if score < 0.55:
        recommendation = "high_risk"

    elif score < 0.7:
        recommendation = "caution"

    result = {

        "timestamp": time.time(),

        "analysis": data,

        "recommendation": recommendation,

        "confidence": round(score, 3)
    }

    return result
