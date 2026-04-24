# =========================
# 👁️ DECISION ENGINE (OBSERVER MODE)
# =========================

from ENGINE.pattern_engine import analyze_pattern

class DecisionEngine:

    def __init__(self):
        pass

    def run(self, data):

        # =========================
        # 👁️ 1. OBSERVE (ไม่ตัดสินก่อน)
        # =========================
        pattern = analyze_pattern(data)

        route = pattern.get("route", "general")

        # =========================
        # 🧠 2. SELECT ENGINE
        # =========================

        try:

            if route == "survival":
                from ENGINE.survival_advisor import advise as engine_func

            elif route == "risk":
                from ENGINE.risk_engine import assess as engine_func

            elif route == "uncertain":
                from ENGINE.consensus_engine import resolve as engine_func

            else:
                from ENGINE.strategy_planner import plan as engine_func

        except Exception as e:
            return {
                "route": route,
                "observer": "fallback",
                "error": f"ENGINE LOAD FAIL: {str(e)}",
                "input": data.get("input")
            }

        # =========================
        # ⚙️ 3. EXECUTE (ผ่าน kernel)
        # =========================

        try:
            result = engine_func(pattern)
        except Exception as e:
            result = {
                "error": f"ENGINE FAIL: {str(e)}"
            }

        # =========================
        # 👁️ 4. RETURN AS OBSERVER
        # =========================

        return {
            "observer": "KING DIADEM",
            "route": route,
            "pattern": pattern,
            "result": result,
            "input": data.get("input")
        }
