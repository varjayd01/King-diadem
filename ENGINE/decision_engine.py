def run_decision(location,food,money,danger):


    score = 0

    score += food * 2
    score += money * 1
    score -= danger * 3


    if score < 0:

        return """
High Risk Situation

Priority:
1. Reduce exposure
2. Secure food
3. Find temporary shelter
"""



    elif score < 10:

        return """
Unstable Condition

Recommended actions:
1. Preserve remaining resources
2. Avoid new risks
3. Search for stable income
"""



    else:

        return """
Stable Situation

Options available:
1. Expand opportunities
2. Build long term resources
3. Reduce dependency risk
"""
