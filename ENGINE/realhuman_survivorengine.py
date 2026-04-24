def survival_check(text: str):

    if "เงิน" in text:
        return {
            "state": "critical",
            "advice": "ลดค่าใช้จ่ายทันที หาเงินระยะสั้น"
        }

    if "หิว" in text:
        return {
            "state": "low_energy",
            "advice": "หาอาหารก่อน ระบบต้องไม่ตัด choice"
        }

    return {
        "state": "normal",
        "advice": "ยังมีทางเลือกอยู่"
    }
