# ENGINE/decision_engine.py

from typing import Dict, Any


class DecisionEngine:
    """
    CORE DECISION ENGINE
    - รับ input + survival state
    - วิเคราะห์ความเสี่ยง
    - คืน 'ทางเลือกที่ยังรอด'
    """

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:

        user_input = data.get("input", "")
        state = data.get("state", {})

        energy = int(state.get("energy", 50))
        food = state.get("food", True)
        safe = state.get("safe_place", True)

        # 🔥 1. ประเมินความเสี่ยง (Risk Scan)
        risk_level = self._assess_risk(energy, food, safe)

        # 🔥 2. สร้างทางเลือก (Choice Generator)
        choices = self._generate_choices(risk_level, energy)

        # 🔥 3. สถานะระบบ
        status = self._status(risk_level)

        return {
            "status": status,
            "risk": risk_level,
            "choices": choices,
            "input_echo": user_input
        }

    # ---------------------

    def _assess_risk(self, energy, food, safe):

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
