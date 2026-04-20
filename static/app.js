async function run() {

    const data = {
        text: document.getElementById("text").value,
        energy: parseFloat(document.getElementById("energy").value),
        food_access: document.getElementById("food").checked,
        safe_place: document.getElementById("safe").checked,
        mental_state: document.getElementById("mental").value
    };

    const res = await fetch("/ENGINE", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const json = await res.json();

    document.getElementById("output").innerText =
        "SURVIVAL:\n" + JSON.stringify(json.survival, null, 2) +
        "\n\nAI:\n" + json.ai;
}
