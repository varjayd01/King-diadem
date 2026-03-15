import random
import time


def analyze_world(context):

    volatility = random.uniform(0.2,0.9)

    trend = "uncertain"

    if volatility < 0.4:
        trend = "stable cycle"

    if volatility > 0.75:
        trend = "high instability"

    return {

        "domain": "world",

        "timestamp": time.time(),

        "analysis": context,

        "global_volatility": round(volatility,3),

        "trend": trend
    }
