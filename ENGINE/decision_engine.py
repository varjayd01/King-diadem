from typing import Dict, Any

# 🔗 เชื่อม ENGINE อื่น
from ENGINE.risk_engine import assess_risk as risk_engine_assess
from ENGINE.pattern_engine import detect_pattern
from ENGINE.council_engine import council_review

# 🔗 เชื่อม CORE
from core.trust_system import evaluate as trust_evaluate


class DecisionEngine:
    """
    CORE DECISION ENGINE (CONNECTED VERSION)
    - รวมทุก engine
    - คืนทางเลือกที่ยังรอดจริง
    """

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:

        user_input = data.get("input", "")
        state = data.get("state", {})

        energy = int(state.get("energy", 50))
        food = state.get("food", True)
        safe = state.get("safe_place", True)

        # 🧠 1. Risk Scan (ใช้ engine ภายนอกก่อน)
        try:
            risk_level = risk_engine_assess(energy, food, safe)
        except:
            risk_level = self._assess_risk_local(energy, food, safe)

        # 🧠 2. Pattern วิเคราะห์พฤติกรรม
        try:
            pattern = detect_pattern(user_input)
        except:
            pattern = "UNKNOWN"

        # 🧠 3. Core Trust Check
        try:
            trust = trust_evaluate()
        except:
            trust = "UNVERIFIED"

        # 🧠 4. สร้างทางเลือก
        choices = self._generate_choices(risk_level, energy)

        # 🧠 5. Council Review (รวมมุมมอง)
        try:
            council = council_review({
                "risk": risk_level,
                "pattern": pattern,
                "choices": choices
            })
        except:
            council = "NO COUNCIL"

        # 🧠 6. สถานะ
        status = self._status(risk_level)

        return {
            "status": status,
            "risk": risk_level,
            "pattern": pattern,
            "trust": trust,
            "council": council,
            "choices": choices,
            "input_echo": user_input
        }

    # ---------------------

    def _assess_risk_local(self, energy, food, safe):

        if energy < 20 or not food or not safe:
            return "HIGH"

        if energy < 50:
            return "MEDIUM"

        return "LOW"

    # ---------------------

    def _generate_choices(self, risk, energy):

        if risk == "HIGH":
            return [
                "หยุดทุกการตัดสินใจที่ไม่จำเป็น",
                "ฟื้นฟูพลังงานทันที",
                "ออกจากสภาพแวดล้อมเสี่ยง"
            ]

        if risk == "MEDIUM":
            return [
                "ลดความเสี่ยงก่อนขยาย",
                "ประเมินทรัพยากรใหม่",
                "เลี่ยงการตัดสินใจใหญ่"
            ]

        return [
            "ดำเนินการต่อได้",
            "สังเกตการเปลี่ยนแปลง",
            "ขยายได้แบบควบคุม"
        ]

    # ---------------------

    def _status(self, risk):

        if risk == "HIGH":
            return "⚠️ SURVIVAL MODE"

        if risk == "MEDIUM":
            return "⚖️ STABLE (LIMITED)"

        return "✅ STABLE"
