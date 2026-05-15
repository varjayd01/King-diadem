# ENGINE/realhuman_survivorengine.py
"""
REAL HUMAN SURVIVOR ENGINE — KING DIADEM
วิเคราะห์สถานะมนุษย์จริง แล้วส่ง context ให้ LYLA ตอบ
ไม่ใช่ hardcode string — engine อ่าน state แล้วบอก LYLA ว่าควรโฟกัสอะไร
"""

from dataclasses import dataclass, field
from typing import Optional


# ── Data structures ───────────────────────────────────────────────

@dataclass
class HumanState:
    energy:          float = 50.0   # 0-100
    money:           float = 0.0    # เงินที่มี (บาท หรือ arbitrary unit)
    food_access:     bool  = True
    safe_place:      bool  = True
    mental_state:    str   = "stable"   # stable / stressed / overwhelmed
    time_available:  float = 8.0    # ชั่วโมงที่มี
    sleep_hours:     float = 6.0    # นอนล่าสุดกี่ชั่วโมง
    days_in_crisis:  int   = 0      # ติดต่อกันกี่วันแล้ว


@dataclass
class SurvivalOutput:
    status:      str
    priority:    str            # สิ่งที่ต้องทำก่อนทุกอย่าง
    context_for_lyla: str       # ★ ส่งให้ LYLA ใช้เป็น context จริง
    waterline:   float          # 0-100 (100 = ปลอดภัย)
    can_decide:  bool           # ตอนนี้ควรตัดสินใจใหญ่ไหม
    flags:       list = field(default_factory=list)


# ── Engine ────────────────────────────────────────────────────────

class RealHumanSurvivorEngine:

    ENERGY_MIN      = 20
    ENERGY_CRITICAL = 10
    SLEEP_MIN       = 4
    CRISIS_LIMIT    = 7  # วัน

    def run(self, state: HumanState) -> SurvivalOutput:
        flags = self._scan_flags(state)
        waterline = self._calc_waterline(state)

        # ── Level 0: overwhelmed — ห้ามตัดสินใจ ──
        if state.mental_state == "overwhelmed" or state.energy < self.ENERGY_CRITICAL:
            return SurvivalOutput(
                status   = "RESET_REQUIRED",
                priority = "หยุดก่อน ร่างกายและจิตใจต้องการ reset",
                context_for_lyla = (
                    f"[SURVIVOR ENGINE] สถานะ: OVERWHELMED | "
                    f"energy={state.energy:.0f} mental={state.mental_state} "
                    f"sleep={state.sleep_hours:.1f}h days_crisis={state.days_in_crisis} | "
                    f"ห้ามตัดสินใจใหญ่ตอนนี้ — ให้ LYLA โฟกัสที่การ stabilize ก่อน "
                    f"ไม่ใช่ให้คำแนะนำเชิงกลยุทธ์ | flags={flags}"
                ),
                waterline  = waterline,
                can_decide = False,
                flags      = flags,
            )

        # ── Level 1: no food / no shelter ──
        if not state.food_access:
            return SurvivalOutput(
                status   = "CRITICAL_NO_FOOD",
                priority = "หาอาหารก่อนทุกอย่าง",
                context_for_lyla = (
                    f"[SURVIVOR ENGINE] ไม่มีอาหาร | energy={state.energy:.0f} money={state.money:.0f} | "
                    f"LYLA ต้องช่วยหาทางได้อาหารทันที ไม่ใช่วางแผนระยะยาว | flags={flags}"
                ),
                waterline  = waterline,
                can_decide = False,
                flags      = flags,
            )

        if not state.safe_place:
            return SurvivalOutput(
                status   = "CRITICAL_NO_SHELTER",
                priority = "หาที่ปลอดภัยก่อน",
                context_for_lyla = (
                    f"[SURVIVOR ENGINE] ไม่มีที่ปลอดภัย | energy={state.energy:.0f} | "
                    f"LYLA ต้องช่วยหาพื้นที่ปลอดภัยก่อน ทุกเรื่องอื่นรอได้ | flags={flags}"
                ),
                waterline  = waterline,
                can_decide = False,
                flags      = flags,
            )

        # ── Level 2: low energy / sleep ──
        if state.energy < self.ENERGY_MIN or state.sleep_hours < self.SLEEP_MIN:
            return SurvivalOutput(
                status   = "LOW_ENERGY",
                priority = "พักก่อน ร่างกายไม่พร้อมทำงาน",
                context_for_lyla = (
                    f"[SURVIVOR ENGINE] พลังงานต่ำ | energy={state.energy:.0f} "
                    f"sleep={state.sleep_hours:.1f}h money={state.money:.0f} | "
                    f"LYLA แนะนำให้พักก่อน อย่าผลักดันให้ตัดสินใจใหญ่ "
                    f"ถ้าต้องทำอะไรให้เลือกอย่างเดียวที่เล็กที่สุดก่อน | flags={flags}"
                ),
                waterline  = waterline,
                can_decide = False,
                flags      = flags,
            )

        # ── Level 3: stressed แต่ยังไหว ──
        if state.mental_state == "stressed" or state.days_in_crisis > 3:
            return SurvivalOutput(
                status   = "STRESSED_FUNCTIONAL",
                priority = "ทำได้แต่ต้องระวัง — จำกัดการตัดสินใจ",
                context_for_lyla = (
                    f"[SURVIVOR ENGINE] stressed แต่ยังทำได้ | "
                    f"energy={state.energy:.0f} days_crisis={state.days_in_crisis} "
                    f"time={state.time_available:.1f}h | "
                    f"LYLA เสนอทางเลือกที่ใช้แรงน้อยก่อน "
                    f"อย่าให้ list ยาว ให้โฟกัสหนึ่งอย่าง | flags={flags}"
                ),
                waterline  = waterline,
                can_decide = True,
                flags      = flags,
            )

        # ── Level 4: stable ──
        return SurvivalOutput(
            status   = "STABLE",
            priority = "พร้อมทำงานปกติ",
            context_for_lyla = (
                f"[SURVIVOR ENGINE] stable | energy={state.energy:.0f} "
                f"time={state.time_available:.1f}h money={state.money:.0f} | "
                f"LYLA วิเคราะห์ได้เต็มที่ เสนอทางเลือกได้หลายทาง | flags={flags}"
            ),
            waterline  = waterline,
            can_decide = True,
            flags      = flags,
        )

    # ── helpers ──────────────────────────────────────────────────

    def _scan_flags(self, state: HumanState) -> list:
        flags = []
        if state.energy < self.ENERGY_CRITICAL:
            flags.append("CRITICAL_ENERGY")
        if state.sleep_hours < self.SLEEP_MIN:
            flags.append("SLEEP_DEBT")
        if not state.food_access:
            flags.append("NO_FOOD")
        if not state.safe_place:
            flags.append("NO_SHELTER")
        if state.days_in_crisis >= self.CRISIS_LIMIT:
            flags.append("CHRONIC_CRISIS")
        if state.money <= 0:
            flags.append("NO_MONEY")
        return flags

    def _calc_waterline(self, state: HumanState) -> float:
        score = 100.0
        score -= max(0, (50 - state.energy))         # energy penalty
        score -= max(0, (6  - state.sleep_hours) * 5) # sleep penalty
        if not state.food_access:  score -= 30
        if not state.safe_place:   score -= 40
        if state.mental_state == "overwhelmed": score -= 25
        if state.mental_state == "stressed":    score -= 10
        score -= min(20, state.days_in_crisis * 2)
        return max(0.0, min(100.0, score))


# ── Parse text input → HumanState ────────────────────────────────
# ให้ app.py เรียกตรงนี้แทนที่จะ construct HumanState เอง

def parse_state_from_context(context: dict) -> HumanState:
    """
    แปลง context dict จาก frontend → HumanState
    ใช้ค่า default ที่สมเหตุสมผลถ้าไม่มีข้อมูล
    """
    return HumanState(
        energy         = float(context.get("energy",         50)),
        money          = float(context.get("money",           0)),
        food_access    = bool(context.get("food_access",   True)),
        safe_place     = bool(context.get("safe_place",    True)),
        mental_state   = str(context.get("mental_state", "stable")),
        time_available = float(context.get("time_available",  8)),
        sleep_hours    = float(context.get("sleep_hours",     6)),
        days_in_crisis = int(context.get("days_in_crisis",    0)),
    )


# ── Monday reset (ยังเก็บไว้) ─────────────────────────────────────

def monday_reset(pleasure_level: float, energy: float) -> dict:
    """
    วิเคราะห์ effect หลัง weekend — ยังคง concept เดิม
    """
    drop = max(0.0, pleasure_level - energy)
    severity = "HIGH" if drop > 30 else "MODERATE" if drop > 15 else "LOW"
    return {
        "effect":   "EMOTIONAL_RESET",
        "drop":     drop,
        "severity": severity,
        "context_for_lyla": (
            f"[MONDAY_RESET] pleasure={pleasure_level:.0f} energy={energy:.0f} "
            f"drop={drop:.0f} severity={severity} | "
            f"LYLA รับรู้ว่าผู้ใช้อาจรู้สึกแย่หลังวันหยุด "
            f"ไม่ผลักดัน ช่วยหา momentum เล็กๆ ก่อน"
        ),
    }
