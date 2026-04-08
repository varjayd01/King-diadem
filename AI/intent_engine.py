def analyze_intent(input_data):
    text = (input_data or "").lower()

    if "ควรทำยังไง" in text or "ทำไงดี" in text:
        return "question"

    if "เงิน" in text or "จน" in text:
        return "survival"

    return "general"
