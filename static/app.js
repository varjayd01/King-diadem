async function sendDecision() {
    const inputText = document.getElementById("input").value;

    const response = await fetch("/api/decision", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            input: inputText,
            state: {
                energy: 50,
                food: true,
                safe_place: true
            }
        })
    });

    const data = await response.json();
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
}
