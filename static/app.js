async function send() {
    const input = document.getElementById("msg")
    const output = document.getElementById("out")

    const msg = input.value.trim()

    if (!msg) {
        output.innerText = "⚠️ กรุณาพิมพ์ข้อความก่อน"
        return
    }

    // 🔒 lock ปุ่มกัน spam
    input.disabled = true

    try {
        const res = await fetch("/decision", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: msg })
        })

        if (!res.ok) {
            throw new Error(`Server error: ${res.status}`)
        }

        const data = await res.json()

        output.innerText = data.reply || "⚠️ ไม่มีคำตอบจากระบบ"

    } catch (err) {
        output.innerText = "❌ ระบบมีปัญหา ลองใหม่อีกครั้ง"
        console.error("ERROR:", err)
    } finally {
        // 🔓 unlock
        input.disabled = false
        input.value = ""
    }
}
