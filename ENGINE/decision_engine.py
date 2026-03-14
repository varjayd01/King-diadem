import random

def run_decision(data):

    if not isinstance(data, dict):
        return {
            "error": "invalid input"
        }

    prompt = data.get("prompt")

    if not prompt:
        return {
            "decision": "No prompt provided"
        }

    prompt = prompt.lower()

    # simple logic layer
    if "money" in prompt:
        return {
            "decision": "Focus on stability before scaling."
        }

    if "relationship" in prompt:
        return {
            "decision": "Clarity first. Emotion second."
        }

    if "risk" in prompt:
        return {
            "decision": "Reduce downside before upside."
        }

    # fallback AI-style decision
    responses = [
        "Gather more information before deciding.",
        "Move slowly and preserve options.",
        "Stability first, expansion later.",
        "Protect resources before action."
    ]

    return {
        "decision": random.choice(responses)
    }
