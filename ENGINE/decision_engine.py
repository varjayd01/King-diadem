from AI.strategic_engine import strategic_analysis


def run_decision(location, food, money, danger):

    analysis = strategic_analysis(location, food, money, danger)

    result = f"""
RISK SCORE: {analysis['risk_score']}

Recommended actions:

"""

    for action in analysis["recommended_actions"]:
        result += f"- {action}\n"

    return result
