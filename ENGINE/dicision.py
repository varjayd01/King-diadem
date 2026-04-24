# =========================
# 🧠 KING DIADEM LIGHT THINKER (AI KERNEL BRIDGE)
# =========================

def think(text: str):

    if not text:
        return "ไม่มี input"

    t = text.lower()

    # =========================
    # 🔥 BASIC HUMAN SURVIVAL
    # =========================
    if "หิว" in t:
        return "⚠️ survival: ไปกินก่อน ระบบจะพังถ้า energy = 0"

    if "เหนื่อย" in t or "ล้า" in t:
        return "⚠️ energy: พักก่อน ไม่งั้น decision จะพัง"

    if "กลัว" in t or "panic" in t:
        return "⚠️ risk: อย่าเพิ่งตัดสินใจตอนนี้"

    # =========================
    # 🔥 SYSTEM MODE
    # =========================
    if "พัง" in t or "ล้ม" in t:
        return "⚠️ collapse detected: ระบบกำลังเข้าสู่ failure chain"

    # =========================
    # 🧠 DEFAULT = OBSERVER
    # =========================
    return f"👁️ observer: รับรู้แล้ว → {text}"
