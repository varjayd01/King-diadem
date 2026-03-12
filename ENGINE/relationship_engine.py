def analyze_relationship(context):

    risk = 0

    if context["depression"]:
        risk += 30

    if context["dependency"]:
        risk += 40

    if context["violence_risk"]:
        risk += 80

    if risk > 80:
        return "collapse_risk"

    if risk > 40:
        return "unstable"

    return "stable"
