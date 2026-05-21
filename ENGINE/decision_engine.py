# ENGINE/decision_engine.py
# KING DIADEM — Decision Engine
# ★ FIX: BLOCKED ไม่ return raw dict แล้ว
#         emotional_flag → route vega + Gemini ยังรัน
#         ไม่มี early return ที่ตัด Gemini ออก

import json
import re

from ENGINE.pattern_engine import analyze_pattern
from core.llm_gemini import GeminiLLM
from core.emptiness_guard import emptiness_guard


class DecisionEngine:

    def __init__(self):
        try:
            self.llm = GeminiLLM(model="gemini-2.5-flash")
            print("✅ DecisionEngine: GeminiLLM loaded")
        except Exception as e:
            print(f"❌ DecisionEngine: GeminiLLM failed - {e}")
            self.llm = None

        try:
            from core.lyla_kernel import LylaKernel
            self.lyla = LylaKernel()
            print("✅ DecisionEngine: LYLA loaded")
        except Exception:
            self.lyla = None

        try:
            from ENGINE.paticcasamuppada_engine import suffering_infrastructure
            self.paticca = suffering_infrastructure
        except Exception:
            self.paticca = None

        try:
            from core.core_loop import run_core
            self.core_loop = run_core
        except Exception:
            self.core_loop = None

    def run(self, data: dict) -> dict:
        user_input = data.get("input") or data.get("text") or ""

        if not user_input:
            return {"observer": "KING DIADEM", "status": "ERROR", "message": "ไม่พบ input"}

        # 1. PATTERN
        pattern = analyze_pattern(data)
        route = pattern.get("route", "general")

        # 2. EMPTINESS GUARD
        guarded = emptiness_guard(pattern)

        # ★ FIX: BLOCK จริงมีแค่ CHOICE_COLLAPSE และ KERNEL_IMPORT_FAIL
        #         กรณีนั้น system พัง ไม่ใช่ผู้ใช้พูดอะไร
        if guarded.get("blocked") and guarded.get("reason") in ("CHOICE_COLLAPSE", "KERNEL_IMPORT_FAIL", "invalid_state"):
            return {
                "observer": "KING DIADEM",
                "route": "BLOCKED",
                "reason": guarded.get("reason", "GUARD_BLOCK"),
                "action": "stabilize",
                "status": "BLOCKED",
                "ai_response": "ระบบพบปัญหาภายใน กรุณาลองใหม่อีกครั้งครับ",
                "risk_score": guarded.get("risk_score", 0),
                "pattern": {
                    "entropy": pattern.get("entropy"),
                    "resource": pattern.get("resource"),
                    "stability": pattern.get("stability"),
                },
            }

        # ★ FIX: emotional_flag → route vega ไม่ block
        if guarded.get("emotional_flag") or guarded.get("suggested_route") == "vega":
            route = "vega"
        elif guarded.get("forced_action") == "stabilize":
            # risk สูง → route survival แต่ยัง run Gemini
            if route not in ("survival", "collapse", "vega"):
                route = "survival"

        # 3. CORE LOOP
        core_result = None
        if self.core_loop:
            try:
                core_result = self.core_loop({
                    "entropy": pattern.get("entropy", 40),
                    "resource": pattern.get("resource", 50),
                    "stability": pattern.get("stability", 60),
                    "drift": 0
                })
                if core_result.get("status") == "HALT" and route not in ("vega",):
                    route = "survival"
            except Exception:
                pass

        # 4. COLLAPSE CHAIN
        paticca_result = None
        if self.paticca:
            try:
                paticca_result = self.paticca(user_input, pattern)
            except Exception:
                pass

        # 5. ENGINE ROUTE
        engine_result = self._run_route(route, pattern)

        # 6. GEMINI — รันเสมอ ไม่มีเงื่อนไขตัดออก
        ai_response = None
        if self.llm:
            try:
                context = (
                    f"Route: {route} | "
                    f"Entropy: {pattern.get('entropy')} | "
                    f"Resource: {pattern.get('resource')} | "
                    f"Stability: {pattern.get('stability')}"
                )
                if guarded.get("emotional_flag"):
                    context += " | EMOTIONAL_FLAG: true — ผู้ใช้อาจอยู่ในสถานการณ์ยาก"
                if paticca_result and paticca_result.get("root_cause"):
                    context += f" | Root: {paticca_result.get('root_cause')}"
                ai_response = self.llm.generate_with_governance(
                    prompt=user_input,
                    additional_context=context
                )
            except Exception as e:
                ai_response = f"[Gemini unavailable: {e}]"

        # 7. LYLA
        lyla_note = None
        if self.lyla:
            try:
                lyla_note = self.lyla.observe(user_input)
            except Exception:
                pass

        return {
            "observer": "KING DIADEM",
            "status": "SUCCESS",
            "route": route,
            "input": user_input,
            "pattern": {
                "entropy": pattern.get("entropy"),
                "resource": pattern.get("resource"),
                "stability": pattern.get("stability"),
                "confidence": pattern.get("confidence"),
                "warnings": pattern.get("warnings", [])
            },
            "engine_result": engine_result,
            "ai_response": ai_response,
            "collapse_chain": paticca_result,
            "core_loop": core_result,
            "lyla": lyla_note,
            "risk_score": guarded.get("risk_score", 0),
            "emotional_flag": guarded.get("emotional_flag", False),
        }

    def _run_route(self, route: str, pattern: dict) -> dict:
        try:
            if route == "survival":
                from ENGINE.survival_advisor import advise
                return advise(pattern)
            elif route == "risk":
                from ENGINE.risk_engine import assess
                return assess(pattern)
            elif route == "collapse":
                from ENGINE.collapse_predictor import analyze
                return analyze(pattern)
            elif route == "uncertain":
                from ENGINE.consensus_engine import resolve
                return resolve(pattern)
            elif route == "civil":
                from ENGINE.civil_work_engine import assess
                return assess(pattern)
            elif route == "vega":
                # vega route — engine ไม่มีอะไรพิเศษ ปล่อย Gemini ทำงาน
                return {"route": "vega", "status": "pass_to_llm"}
            else:
                from ENGINE.strategy_planner import plan
                return plan(pattern)
        except Exception as e:
            return {"error": f"ENGINE ROUTE FAIL [{route}]: {str(e)}"}


# ── Singleton ──────────────────────────────────────────────────────
_ENGINE_SINGLETON = None


def _engine() -> "DecisionEngine":
    global _ENGINE_SINGLETON
    if _ENGINE_SINGLETON is None:
        _ENGINE_SINGLETON = DecisionEngine()
    return _ENGINE_SINGLETON


def _build_payload(data: dict) -> dict:
    out = dict(data) if isinstance(data, dict) else {}
    text = str(out.get("input") or out.get("text") or out.get("question") or "").strip()
    if not text:
        parts = []
        for k, label in [("location", "ที่ตั้ง"), ("food", "อาหาร"), ("money", "เงิน"), ("risk", "ความเสี่ยง")]:
            v = out.get(k)
            if v not in (None, "", "unknown"):
                parts.append(f"{label}: {v}")
        text = " | ".join(parts)
    out["input"] = text

    if "money" in out:
        try:
            m = abs(float(out["money"]))
            out.setdefault("resource", max(5.0, min(95.0, 100.0 - min(m, 99.0))))
        except (TypeError, ValueError):
            pass

    risk_s = str(out.get("risk", "")).lower()
    if any(w in risk_s for w in ["high", "สูง", "critical"]):
        try:
            out["entropy"] = min(95.0, float(out.get("entropy", 40)) + 20.0)
        except (TypeError, ValueError):
            out["entropy"] = 65.0

    return out


def eternal_snapshot_for_decision(state: dict) -> dict:
    try:
        from ENGINE.eternal_runtime import eternal_snapshot
        return eternal_snapshot(state)
    except Exception as e:
        return {"error": str(e)}


def run_decision(data):
    if not isinstance(data, dict):
        data = {"input": str(data)}

    merged = _build_payload(data)
    if not (merged.get("input") or "").strip():
        return {
            "observer": "KING DIADEM",
            "status": "ERROR",
            "message": "ไม่พบ input",
        }

    merged["_eternal_snapshot"] = eternal_snapshot_for_decision({
        "entropy": float(merged.get("entropy", 40)),
        "resource": float(merged.get("resource", 50)),
        "stability": float(merged.get("stability", 60)),
    })

    try:
        from ENGINE.self_learning import analyze_patterns
        merged["_learning_patterns"] = analyze_patterns()
    except Exception:
        merged["_learning_patterns"] = None

    try:
        from ENGINE.human_engine import analyze_human
        merged["_human_engine"] = analyze_human(
            {"state": merged.get("input", ""), "context": merged.get("intent")}
        )
    except Exception:
        merged["_human_engine"] = None

    result = _engine().run(merged)
    return result


def decide(input=None, intent=None, risk=None, **kwargs):
    chunks = []
    if input is not None:
        chunks.append(str(input))
    if intent is not None:
        chunks.append("บริบท: " + (json.dumps(intent, ensure_ascii=False) if isinstance(intent, dict) else str(intent)))
    if risk is not None:
        chunks.append("ความเสี่ยง: " + (json.dumps(risk, ensure_ascii=False) if isinstance(risk, dict) else str(risk)))
    for k, v in kwargs.items():
        if v is not None:
            chunks.append(f"{k}: {v}")
    return run_decision({"input": "\n".join(chunks).strip()})


def generate_choices(location, food, money, risk):
    body = {
        "input": (
            f"เสนอทางเลือก 3–5 ข้อ สั้น กระชับ "
            f"บริบท: ที่ตั้ง {location} อาหาร {food} เงิน {money} ความเสี่ยง {risk}"
        )
    }
    out = run_decision(body)
    ai = out.get("ai_response") or ""
    lines = [re.sub(r"^[\d\.\)\-\*•]+\s*", "", s.strip())
             for s in str(ai).splitlines() if len(s.strip()) > 3]
    if len(lines) >= 3:
        return lines[:10]
    return [
        "แยกปัญหาเป็น วันนี้ / สัปดาห์นี้ / เดือนนี้ แล้วทำแค่วันนี้ก่อน",
        "หาตัวเลขขั้นต่ำที่ต้องมี แล้วลดรายจ่ายอื่นชั่วคราว",
        "ถ้าเสี่ยงสูง อย่าตัดสินใจถาวรวันนี้ เลือกแค่ปลอดภัยชั่วคราว",
        "ติดต่อคนที่ไว้ใจได้หนึ่งคน ขอให้ช่วยฟังหรือช่วยคิด",
    ]


def decision_intelligence(state, risk):
    state = state if isinstance(state, dict) else {}
    risk = risk if isinstance(risk, dict) else {}
    level = str(risk.get("level", "MEDIUM")).upper()
    try:
        score = float(risk.get("risk_score", 0))
    except (TypeError, ValueError):
        score = 0.0
    try:
        res = float(state.get("resource", 50))
    except (TypeError, ValueError):
        res = 50.0
    try:
        stab = float(state.get("stability", 60))
    except (TypeError, ValueError):
        stab = 60.0

    if level == "CRITICAL" or score >= 85 or res <= 10:
        return {"action": "stabilize", "message": "ชะลอการตัดสินใจใหญ่ — ดูแลพื้นฐานก่อน"}
    if level == "HIGH" or score >= 60 or stab < 35:
        return {"action": "stabilize", "message": "แยกปัญหาเป็นขั้นเล็กๆ แล้วทำทีละขั้น"}
    if res < 30:
        return {"action": "recover_resource", "message": "ทรัพยากรต่ำ — เลือกสิ่งจำเป็นก่อน"}
    if stab < 45:
        return {"action": "expand_choices", "message": "หาทางเลือกเสริม 2–3 แบบก่อนตัดสินใจ"}
    return {"action": "maintain", "message": "ไปต่อได้ — รักษาจังหวะพอประมาณ"}
