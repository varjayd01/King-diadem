def estimate_resources(food, money):

    resources = {
        "food_level": food,
        "money_level": money,
        "survival_days": 0
    }

    if food >= 5:
        resources["survival_days"] += 5
    elif food >= 2:
        resources["survival_days"] += 2
    else:
        resources["survival_days"] += 1

    if money >= 1000:
        resources["survival_days"] += 5
    elif money >= 200:
        resources["survival_days"] += 2

    return resources
