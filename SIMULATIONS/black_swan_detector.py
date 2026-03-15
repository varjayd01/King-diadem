import random


def detect_black_swan():

    probability = random.random()

    if probability > 0.97:

        return {
            "black_swan": True,
            "event": "rare systemic disruption"
        }

    return {
        "black_swan": False
    }
