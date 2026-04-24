from typing import Dict, Any

# import engine เฉพาะตอนใช้ (lazy load เพื่อลดโหลด)

class SystemOrchestrator:

    def route(self, user_input: str) -> str:

        text = user_input.lower()

        if "เงิน" in text or "จน" in text:
            return "survival"

        if "เสี่ยง" in text or "อันตราย" in text:
            return "risk"

        if "ความสัมพันธ์" in text:
            return "relationship"

        return "general"

    def execute(self, route: str, data: Dict[str, Any]):

        try:
            if route == "survival":
                from ENGINE.survival_advisor import advise
                return advise(data)

            if route == "risk":
                from ENGINE.risk_engine import assess_risk
                return assess_risk(
                    data["state"]["energy"],
                    data["state"]["food"],
                    data["state"]["safe_place"]
                )

            if route == "general":
                from ENGINE.pattern_engine import detect_pattern
                return detect_pattern(data["input"])

        except Exception as e:
            return f"CORE_FAIL: {str(e)}"

        return "NO_ROUTE"
