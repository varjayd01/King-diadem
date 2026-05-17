import re


class PersonaEngine:
    """
    KING DIADEM — PersonaEngine
    ตรวจ intent + style จากข้อความ
    เชื่อมกับ LYLA Kernel waterline signal
    Fail less. Harm less. Restore more.
    """

    # ── INTENT KEYWORDS ─────────────────────────────────────────
    INTENT_MAP = [
        ("crisis", [
            # TH
            "ฆ่า", "ตาย", "ไม่อยากอยู่", "จบแล้ว", "หมดแล้ว", "สิ้นหวัง",
            "ทนไม่ไหว", "ทรมาน", "หายไป", "หมดหวัง", "ไม่มีทางออก",
            # EN
            r"\bkill\b", r"\bdie\b", r"\bsuicide\b", r"\bhopeless\b",
            r"\bcan't go on\b", r"\bend it\b",
        ]),
        ("survival", [
            # TH
            "ตกงาน", "ไม่มีเงิน", "หนี้", "ค่าเช่า", "กินข้าวไม่ได้",
            "ทรัพยากรหมด", "อยู่ไม่ได้", "รอดยาก", "ฉุกเฉิน", "พังหมด",
            # EN
            r"\bsurvive\b", r"\bdanger\b", r"\bescape\b", r"\bno money\b",
            r"\bbankrupt\b", r"\bevicted\b",
        ]),
        ("business", [
            # TH
            "ธุรกิจ", "บริษัท", "ตลาด", "หุ้น", "ลงทุน", "กำไร", "ขาดทุน",
            "เงินทุน", "พนักงาน", "ลูกค้า", "ยอดขาย", "startup",
            # EN
            r"\bmoney\b", r"\bmarket\b", r"\bbusiness\b", r"\binvest\b",
            r"\brevenue\b", r"\bprofit\b",
        ]),
        ("life", [
            # TH
            "ความสัมพันธ์", "แฟน", "ครอบครัว", "เพื่อน", "ชีวิต",
            "อนาคต", "ความฝัน", "ตัวตน", "เครียด", "เหนื่อย",
            # EN
            r"\blife\b", r"\brelationship\b", r"\bfamily\b", r"\bfriend\b",
        ]),
    ]

    # ── STYLE KEYWORDS ──────────────────────────────────────────
    STYLE_MAP = [
        ("playful",  ["เริ่ด", "โคตร", "มึง", "กู", "ว้าว", "555", "lol", "haha"]),
        ("formal",   ["ครับ", "ค่ะ", "กรุณา", "ขอบคุณ", "เรียน"]),
        ("urgent",   ["ด่วน", "ตอนนี้", "ทันที", "เร่งด่วน", "asap", "urgent"]),
        ("confused", ["ไม่รู้", "ไม่แน่ใจ", "งง", "confused", "stuck", "ไม่เข้าใจ"]),
    ]

    # ── WATERLINE SIGNAL ────────────────────────────────────────
    WATERLINE_MAP = {
        "crisis":   "BREACHED",
        "survival": "AT_RISK",
        "business": "NOMINAL",
        "life":     "DECLINING",
        "general":  "NOMINAL",
    }

    CHOICE_FLOOR_MAP = {
        "crisis":   0,   # Choice → 0: Intervene ทันที
        "survival": 1,   # Choice ≥ 1: Monitor
        "business": 2,
        "life":     1,
        "general":  3,
    }

    # ────────────────────────────────────────────────────────────

    def detect_intent(self, text: str) -> str:
        t = text.lower()
        for intent, patterns in self.INTENT_MAP:
            for pat in patterns:
                if re.search(pat, t):
                    return intent
        return "general"

    def detect_style(self, text: str) -> str:
        t = text.lower()
        for style, keywords in self.STYLE_MAP:
            for kw in keywords:
                if kw in t:
                    return style
        return "neutral"

    def observe(self, text: str) -> dict:
        """
        Full LYLA-aligned observation
        คืน waterline + choice_floor + action signal
        """
        intent = self.detect_intent(text)
        style  = self.detect_style(text)
        wl     = self.WATERLINE_MAP.get(intent, "NOMINAL")
        floor  = self.CHOICE_FLOOR_MAP.get(intent, 2)

        # ── ACTION SIGNAL ──
        if intent == "crisis":
            action = "INTERVENE"
            note   = "Choice collapse risk. Stop-the-Line activated. คืนทางออกก่อนทุกอย่าง"
        elif intent == "survival":
            action = "STABILIZE"
            note   = "Waterline at risk. ระบุทรัพยากรที่มีจริงก่อน optimize"
        elif wl == "DECLINING":
            action = "MONITOR"
            note   = "Drift accumulating. Measure before act."
        else:
            action = "OBSERVE"
            note   = "No critical signal. Silence = alignment preserved."

        return {
            "intent":       intent,
            "style":        style,
            "waterline":    wl,
            "choice_floor": floor,
            "action":       action,
            "note":         note,
            "law":          "Fail less. Harm less. Restore more.",
        }
