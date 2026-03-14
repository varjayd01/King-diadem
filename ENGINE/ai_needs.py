def ai_needs(context):

    needs = []

    if "numbers" not in context:
        needs.append("clarify_quantity")

    if context.get("topic") == "money":
        needs.append("financial_precision")

    if context.get("topic") == "food":
        needs.append("resource_detail")

    return needs
