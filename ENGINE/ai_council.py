# ENGINE/ai_council.py

import random

def ai_council(location, food, money, risk):

    votes = []

    # AI 1 – survival logic
    if money < food:
        votes.append("conserve_money")
    else:
        votes.append("buy_food")

    # AI 2 – risk logic
    if risk == "high":
        votes.append("avoid_action")
    else:
        votes.append("proceed")

    # AI 3 – entropy logic
    if money < 50:
        votes.append("minimal_spending")
    else:
        votes.append("balanced")

    # AI 4 – exploration
    votes.append(random.choice(["explore", "stay"]))

    return votes
