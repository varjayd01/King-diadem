# core/system_orchestrator.py
"""
KING DIADEM — System Orchestrator v2.0
ตัวกลางจริง: route → engine → LLM context
เชื่อม realhuman_survivorengine + vega + parables + llm_gemini
"""
from typing import Dict, Any, Optional


class SystemOrchestrator:

    def route(self, user_input: str, voice_mode: str = "lyla") -> str:
        """อ่าน input แล้วตัดสินใจว่าจะใช้ engine ไหน"""
        t = (user_input or "").lower()

        # crisis ก่อนทุกอย่าง
        crisis_kw = ["อยากตาย","ไม่อยากอยู่","ฆ่าตัว","จบชีวิต","suicid"]
        if any(w in t for w in crisis_kw) or voice_mode == "crisis":
            return "crisis"

        # emotion
        emotion_kw = ["เครียด","ท้อ","เสียใจ","หมดหวัง","เหนื่อย","กลัว","ร้องไห้","โดดเดี่ยว"]
        if any(w in t for w in emotion_kw) or voice_mode == "vega":
            return "vega"

        # survival floor — อาหาร ที่พัก เงินติดลบ
        survival_kw = ["ไม่มีกิน","ไม่มีเงิน","หิว","หมดเงิน","ไม่มีที่อยู่","ถูกไล่ออก","ตกงาน","จน","หนี้"]
        if any(w in t for w in survival_kw):
            return "survival"

        # risk
        risk_kw = ["เสี่ยง","อันตราย","ล้มละลาย","พัง","collapse","ขาดทุน","เจ๊ง"]
        if any(w in t for w in risk_kw):
            return "risk"

        # relationship
        rel_kw = ["แฟน","เลิก","ทะเลาะ","ครอบครัว","พ่อ","แม่","ความสัมพันธ์","เพื่อน"]
        if any(w in t for w in rel_kw):
            return "relationship"

        # business / work
        biz_kw = ["ธุรกิจ","บริษัท","งาน","ลูกค้า","โปรเจกต์","เจ้านาย","ลาออก"]
        if any(w in t for w in biz_kw):
            return "civil"

        return "general"

    def execute(self, route: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        รัน engine ที่เหมาะสม → คืน dict พร้อม context_for_lyla
        ทุก engine ล้มก็ยังคืน dict ที่ใช้ได้
        """
        user_input  = data.get("input", "")
        context     = data.get("context", {})
        history     = data.get("history", [])
        voice_mode  = data.get("voice_mode", "lyla")

        result = {
            "route":           route,
            "context_for_lyla": "",
            "pattern":         {"entropy": 40, "stability": 60, "resource": 50},
            "risk_score":      10.0,
            "can_decide":      True,
            "waterline":       70.0,
            "flags":           [],
            "ai_response":     None,   # None = ให้ LLM ตอบเอง
        }

        ctx_parts = []

        # ── 1. RealHuman SurvivorEngine (ทุก route ใช้) ─────────
        try:
            from ENGINE.realhuman_survivorengine import (
                RealHumanSurvivorEngine, parse_state_from_context
            )
            h_state  = parse_state_from_context(context)
            survival = RealHumanSurvivorEngine().run(h_state)
            result["waterline"]  = survival.waterline
            result["can_decide"] = survival.can_decide
            result["flags"]      = survival.flags
            if survival.context_for_lyla:
                ctx_parts.append(survival.context_for_lyla)
        except Exception as e:
            ctx_parts.append(f"[SURVIVOR_ENGINE_SKIP: {e}]")

        # ── 2. Route-specific engines ────────────────────────────
        if route == "survival":
            try:
                from ENGINE.survival_advisor import advise
                r = advise(data)
                if r: ctx_parts.append(f"[SURVIVAL] {r}")
            except Exception as e:
                ctx_parts.append(f"[SURVIVAL_SKIP: {e}]")

        elif route == "risk":
            try:
                from ENGINE.risk_engine import assess_risk
                state = context.get("state", {})
                r = assess_risk(
                    state.get("energy", 50),
                    state.get("food", True),
                    state.get("safe_place", True)
                )
                if r: ctx_parts.append(f"[RISK] {r}")
                # collapse predictor
                from ENGINE.collapse_predictor import CollapsePredictor
                col = CollapsePredictor().predict(user_input, context)
                if isinstance(col, dict) and col.get("chain"):
                    ctx_parts.append(f"[COLLAPSE_CHAIN] {col['chain']}")
            except Exception as e:
                ctx_parts.append(f"[RISK_SKIP: {e}]")

        elif route in ("vega", "crisis"):
            try:
                from core.vega_mode import vega_mode_hint
                hint = vega_mode_hint(user_input)
                if hint: ctx_parts.append(hint)
            except Exception as e:
                ctx_parts.append(f"[VEGA_SKIP: {e}]")

        elif route == "relationship":
            ctx_parts.append("[RELATIONSHIP] เรื่องความสัมพันธ์ — ฟังก่อน ไม่ตัดสิน")

        elif route == "civil":
            try:
                from ENGINE.strategy_planner import StrategyPlanner
                strat = StrategyPlanner().plan(user_input, context)
                if isinstance(strat, dict) and strat.get("options"):
                    opts = strat["options"][:3]
                    ctx_parts.append(f"[STRATEGY] {' | '.join(str(o) for o in opts)}")
            except Exception as e:
                ctx_parts.append(f"[STRATEGY_SKIP: {e}]")

        else:  # general
            try:
                from ENGINE.pattern_engine import detect_pattern
                pat = detect_pattern(user_input)
                if isinstance(pat, dict):
                    result["pattern"].update({k: v for k, v in pat.items() if v is not None})
            except Exception:
                pass

        # ── 3. Parable injection (ทุก route) ─────────────────────
        try:
            from core.parables import parable_context_note
            p = parable_context_note(user_input)
            if p: ctx_parts.append(p)
        except Exception:
            pass

        # ── 4. Escape routes ถ้า risk สูง ────────────────────────
        if result["risk_score"] > 55 or not result["can_decide"]:
            try:
                from ENGINE.escape_routes import assess
                esc = assess(user_input)
                if esc: ctx_parts.append(f"[ESCAPE_ROUTES] {esc}")
            except Exception:
                pass

        result["context_for_lyla"] = "\n".join(p for p in ctx_parts if p)
        return result

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point จาก app.py
        data = { input, route, voice_mode, history, context, ... }
        """
        user_input = data.get("input", "")
        voice_mode = data.get("voice_mode", "lyla")

        # auto-route ถ้า route เป็น general หรือไม่มี
        route = data.get("route") or "general"
        if route == "general":
            route = self.route(user_input, voice_mode)

        result = self.execute(route, data)

        # ── เรียก LLM ──────────────────────────────────────────
        if result.get("ai_response") is None:
            try:
                from core.llm_gemini import GeminiLLM
                llm = GeminiLLM(model="gemini-2.0-flash")
                result["ai_response"] = llm.generate_with_governance(
                    prompt             = user_input,
                    additional_context = result["context_for_lyla"],
                    history            = data.get("history", []),
                    route              = route,
                    voice_mode         = voice_mode,
                )
            except Exception as e:
                result["ai_response"] = f"[LLM Error: {e}]"

        result["route"]      = route
        result["status"]     = "SUCCESS"
        result["observer"]   = "KING DIADEM"
        result["governance"] = {
            "intent":      {"intent": route, "confidence": 0.8},
            "human_state": result.get("pattern", {}),
        }
        return result


# singleton
_orchestrator: Optional[SystemOrchestrator] = None

def get_orchestrator() -> SystemOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = SystemOrchestrator()
    return _orchestrator
