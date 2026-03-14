def detect_language(text):

    if any(c in text for c in "กขคง"):
        return "th"

    if any(c in text for c in "あいうえお"):
        return "jp"

    return "en"
