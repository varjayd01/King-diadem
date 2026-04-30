# =========================
# 👁️ KING DIADEM DECISION ENGINE (OBSERVER KERNEL)
# =========================

from ENGINE.pattern_engine import analyze_pattern
from core.llm_gemini import GeminiLLM   # ← เพิ่มการ import

class DecisionEngine:

    def __init__(self):
        """Initialize Decision Engine with GeminiLLM"""
        try:
            self.llm = GeminiLLM(model="gemini-2.5-flash")
            print("✅ DecisionEngine: GeminiLLM loaded successfully")
        except Exception as e:
            print(f"❌ DecisionEngine: Failed to load GeminiLLM - {e}")
            self.llm = None

    def run(self, data: dict):
        """
        Main entry point สำหรับ Decision Engine
        """
        user_input = data.get("input") or data.get("text") or ""

        if not user_input:
            return {
                "observer": "KING DIADEM",
                "status": "ERROR",
                "message": "ไม่พบ input"
            }

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
            # ส่ง llm ไปให้ engine_func ใช้ (สำคัญ!)
            if self.llm:
                result = engine_func(pattern, self.llm)
            else:
                result = engine_func(pattern)  # fallback ถ้า llm โหลดไม่ได้

        except Exception as e:
            print(f"Engine execution error on route '{route}': {e}")
            result = {"error": f"ENGINE FAIL: {str(e)}"}

        # =========================
        # 👁️ 4. RETURN
        # =========================
        return {
            "observer": "KING DIADEM",
            "route": route,
            "pattern": pattern,
            "result": result,
            "input": user_input,
            "status": "SUCCESS" if "error" not in result else "ERROR"
        }
