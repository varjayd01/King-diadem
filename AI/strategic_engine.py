"""
KING DIADEM
Strategic Engine

Core rule:
Preserve life.
Avoid harm.
Seek cooperation before conflict.
"""


SAFETY_RULE = """
All strategies must preserve life and avoid harm.

Forbidden:
- Violence
- War
- Harm to people
- Harm to animals
- Destruction of property
- Environmental damage

Preferred:
- Cooperation
- Stability
- Survival
- Restoration
"""


def strategic_analysis(location, food, money, danger):

    risk = (danger * 2) - food

    options = []

    # survival layer

    if food <= 1:
        options.append(
            "Secure food through safe and legal sources such as local markets or community support"
        )

    if money <= 100:
        options.append(
            "Search for short term income opportunities or cooperative work"
        )

    # safety layer

    if danger >= 7:
        options.append(
            "Reduce exposure to danger and relocate to a safer environment"
        )

    # stability layer

    if risk < 5:
        options.append(
            "Expand opportunity carefully while maintaining safety"
        )

    # cooperation layer

    options.append(
        "Seek cooperation with local people or networks before escalating any conflict"
    )

    options.append(
        "Prioritize solutions that protect people, animals, property and environment"
    )

    if not options:
        options.append(
            "Maintain stability, observe the situation and avoid unnecessary risk"
        )

    return {
        "risk_score": risk,
        "location": location,
        "recommended_actions": options,
        "principle": "Survival without harm"
    }
