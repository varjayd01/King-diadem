import random
import time

def analyze_life(context):

    happiness = random.uniform(0.3, 0.9)
    stress = random.uniform(0.2, 0.8)

    direction = "balanced"

    if happiness > 0.75:
        direction = "positive path"

    if stress > 0.7:
        direction = "high stress risk"

    return {

        "domain": "life",

        "timestamp": time.time(),

        "analysis": context,

        "life_balance": round(happiness - stress, 3),

        "direction": direction
    }
