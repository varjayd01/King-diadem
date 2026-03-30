async function send() {
    const input = document.getElementById("input").value;

    const res = await fetch("/api/decision", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ input })
    });

    const data = await res.json();

    document.getElementById("result").innerText = data.output;
}
