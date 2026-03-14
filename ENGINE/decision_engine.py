import random

# dialogue layer
from ENGINE.dialogue_engine import generate_reply

# ai council
from ENGINE.ai_council import ai_council


def run_decision(data):

    """
    Core decision engine
    """

    location = data.get("location")
    food = data.get("food")
    money = data.get("money")
    risk = data.get("risk")

    votes = ai_council(location, food, money, risk)

    decision = random.choice(votes)

    return decision


def dialogue_layer(user_text):

    """
    Human ↔ AI conversation layer
    """

    reply = generate_reply(user_text)

    return {
        "type": "dialogue",
        "reply": reply
    }
