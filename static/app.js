async function runDecision() {
    const input = document.getElementById("inputBox").value;
    const energy = document.getElementById("energy").value;
    const food = document.getElementById("food").checked;
    const safe = document.getElementById("safe").checked;
    const mode = document.getElementById("mode").value;

    const res = await fetch("/decision", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            input: input,
            energy: energy,
            food: food,
            safe: safe,
            mode: mode
        })
    });

    const data = await res.json();

    document.getElementById("output").innerText = data.result;
}
