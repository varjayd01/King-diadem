import re

EMOTION_PATTERNS = {
    "joking": ["555", "ฮ่า", "ขำ", "ตลก"],
    "stress": ["เหนื่อย", "ไม่ไหว", "พัง", "แย่"],
    "hope": ["หวัง", "อยาก", "ลอง"],
    "love": ["รัก", "คิดถึง"],
    "money_problem": ["เงิน", "จน", "หาเงิน"],
}

def detect_emotion(text):

    text = text.lower()

    for emotion, words in EMOTION_PATTERNS.items():
        for w in words:
            if w in text:
                return emotion

    return "neutral"


def extract_context(text):

    context = {}

    numbers = re.findall(r'\d+', text)
    if numbers:
        context["numbers"] = numbers

    if "เงิน" in text:
        context["topic"] = "money"

    if "อาหาร" in text:
        context["topic"] = "food"

    return context
