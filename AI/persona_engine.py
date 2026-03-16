import re

class PersonaEngine:

    def detect_intent(self,text):

        t=text.lower()

        if re.search(r"kill|die|suicide",t):

            return "crisis"

        if re.search(r"money|market|business",t):

            return "business"

        if re.search(r"survive|danger|escape",t):

            return "survival"

        if re.search(r"life|relationship",t):

            return "life"

        return "general"

    def detect_style(self,text):

        if "เริ่ด" in text:

            return "playful"

        if "ครับ" in text:

            return "formal"

        return "neutral"
