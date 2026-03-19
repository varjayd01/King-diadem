def decision_engine(q, profile):

    tone = profile.get("tone", "normal")

    if "เครียด" in q or "เงิน" in q:
        return "หนูอยู่ตรงนี้นะคะ ค่อยๆแก้ไปทีละขั้น พี่ยังมีทางเลือกเสมอค่ะ ❤️"

    if tone == "fun":
        return "วันนี้ต้องปังนะ! 🔥✨ " + q

    return f"🧠 วิเคราะห์: {q}"

# 📊 วิเคราะห์ระบบ
def analyze_system(logs):

    total = len(logs)

    return f"""
📊 SYSTEM

Total Decisions: {total}

📌 Insight:
ผู้ใช้กำลังใช้ระบบต่อเนื่อง
ควรเพิ่มความแม่นยำเฉพาะบุคคล
"""
