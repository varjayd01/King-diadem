def optimize_choice(actions):

    ranked = []

    score = 100

    for action in actions:

        ranked.append({

            "action": action,
            "expected_score": score

        })

        score -= 10

    return ranked
