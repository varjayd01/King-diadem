async function run() {
    const input = document.getElementById("input").value;
    const energy = document.getElementById("energy").value;
    const food = document.getElementById("food").checked;
    const safe = document.getElementById("safe").checked;
    const mode = document.getElementById("mode").value;

    const fullPrompt = `
User Situation:
${input}

Energy: ${energy}
Food: ${food}
Safe: ${safe}
Mode: ${mode}

Give decision advice.
`;

    document.getElementById("result").innerText = "Thinking...";

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: fullPrompt })
        });

        const data = await res.json();
        document.getElementById("result").innerText =
            data.reply || data.error;

    } catch (err) {
        document.getElementById("result").innerText = err;
    }
}
