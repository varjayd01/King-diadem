// static/app.js

async function run() {
    const inputEl = document.getElementById("input");
    const outputEl = document.getElementById("output");

    const text = inputEl.value.trim();

    if (!text) {
        outputEl.textContent = "กรุณาพิมพ์สถานการณ์ก่อน";
        return;
    }

    // แสดงสถานะ
    outputEl.textContent = "KING is thinking...";

    try {
        const response = await fetch("/ENGINE", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                input: text,
                entropy: 40,
                resource: 50,
                stability: 60
            })
        });

        // เช็ค response
        if (!response.ok) {
            throw new Error("HTTP " + response.status);
        }

        const data = await response.json();

        // 👉 แสดงผลแบบอ่านได้ ไม่ใช่กอง JSON ขยะ
        renderOutput(data);

    } catch (err) {
        outputEl.textContent = "ERROR: " + err.message;
    }
}


// 🧠 render ให้มันมีค่า ไม่ใช่ dump เฉย ๆ
function renderOutput(data) {
    const outputEl = document.getElementById("output");

    if (data.status === "error") {
        outputEl.textContent = "ERROR: " + data.message;
        return;
    }

    let text = "";

    // 🧠 decision
    if (data.decision) {
        text += "=== DECISION ===\n";

        text += "Action: " + (data.decision.action || "-") + "\n";
        text += "Message: " + (data.decision.message || "-") + "\n\n";

        if (data.decision.alternatives) {
            text += "Alternatives:\n";
            data.decision.alternatives.forEach((alt, i) => {
                text += "- " + (alt.text || alt.action || "option") + "\n";
            });
            text += "\n";
        }
    }

    // ⚠️ risk
    if (data.risk) {
        text += "=== RISK ===\n";
        text += JSON.stringify(data.risk, null, 2) + "\n\n";
    }

    // 🏛 council
    if (data.council) {
        text += "=== COUNCIL ===\n";
        text += "Members: " + (data.council.council_size || "-") + "\n\n";
    }

    // fallback
    if (text === "") {
        text = JSON.stringify(data, null, 2);
    }

    outputEl.textContent = text;
}
