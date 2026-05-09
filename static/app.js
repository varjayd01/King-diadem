// static/app.js — KING DIADEM core logic

async function run() {
    const inputEl = document.getElementById("input");
    const outputEl = document.getElementById("output");
    const text = inputEl ? inputEl.value.trim() : "";

    if (!text) {
        if (outputEl) outputEl.innerText = "⚠ กรุณาพิมพ์สถานการณ์ก่อน";
        return;
    }

    if (outputEl) outputEl.innerText = "⚡ Running Decision Engine...";

    try {
        const res = await fetch("/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input: text })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        if (data.error) {
            if (outputEl) outputEl.innerText = "❌ " + data.error;
            return;
        }

        if (outputEl) {
            if (data.ai_response) {
                outputEl.innerText = `[${(data.route || "ENGINE").toUpperCase()}]\n\n${data.ai_response}`;
            } else {
                outputEl.innerText = JSON.stringify(data, null, 2);
            }
        }

        const routeTag = document.getElementById("route-tag");
        if (routeTag) routeTag.textContent = `→ route: ${data.route || "general"} | risk: ${Math.round(data.risk_score || 0)}`;

    } catch (err) {
        console.error(err);
        if (outputEl) outputEl.innerText = "🚫 SYSTEM ERROR\n" + err;
    }
}
