async function sendInput() {
    const input = document.getElementById("input").value;

    const res = await fetch("/api/decision", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ input })
    });

    const data = await res.json();

    document.getElementById("output").innerText = data.output;
}
