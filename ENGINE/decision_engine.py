# =========================
# 👁️ KING DIADEM DECISION ENGINE (OBSERVER KERNEL)
# =========================

from ENGINE.pattern_engine import analyze_pattern

class DecisionEngine:

    def run(self, data):

        # =========================
        # 👁️ 1. OBSERVE
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

            elif route == "collapse":
                from ENGINE.collapse_predictor import analyze as engine_func

            elif route == "uncertain":
                from ENGINE.consensus_engine import resolve as engine_func

            else:
                from ENGINE.strategy_planner import plan as engine_func

        except Exception as e:
            return {
                "observer": "KING DIADEM",
                "route": route,
                "error": f"ENGINE LOAD FAIL: {str(e)}"
            }

        # =========================
        # ⚙️ 3. EXECUTE
        # =========================
        try:
            result = engine_func(pattern)
        except Exception as e:
            result = {"error": f"ENGINE FAIL: {str(e)}"}

        # =========================
        # 👁️ 4. RETURN
        # =========================
        return {
            "observer": "KING DIADEM",
            "route": route,
            "pattern": pattern,
            "result": result,
            "input": data.get("input")
        }
