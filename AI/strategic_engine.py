def strategic_analysis(location, food, money, danger):

    risk = danger * 2 - food

    options = []

    if food <= 1:
        options.append("Secure food immediately")

    if money <= 100:
        options.append("Search short term income")

    if danger >= 7:
        options.append("Reduce exposure and relocate")

    if risk < 5:
        options.append("Expand opportunity carefully")

    if not options:
        options.append("Maintain stability and observe")

    return {
        "risk_score": risk,
        "recommended_actions": options
    }
