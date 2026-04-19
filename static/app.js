async function runEngine() {

    const input = document.getElementById("inputBox").value;
    const energy = document.getElementById("energy").value;

    const output = document.getElementById("output");
    output.innerText = "⏳ Running...";

    try {
        const res = await fetch("/ENGINE", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                input: input,
                state: {
                    energy: energy,
                    food: true,
                    safe_place: true
                }
            })
        });

        const data = await res.json();

        output.innerText = JSON.stringify(data, null, 2);

    } catch (err) {
        output.innerText = "❌ ERROR: " + err;
    }
}
