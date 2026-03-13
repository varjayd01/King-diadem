# KING DIADEM Resource Estimator

def estimate_resources(food, money):

    resources = {
        "food": food,
        "money": money,
        "survival_days": 0
    }

    # food impact
    if food >= 5:
        resources["survival_days"] += 5
    elif food >= 2:
        resources["survival_days"] += 2
    else:
        resources["survival_days"] += 1

    # money impact
    if money >= 1000:
        resources["survival_days"] += 5
    elif money >= 200:
        resources["survival_days"] += 2
    else:
        resources["survival_days"] += 0

    return resources
