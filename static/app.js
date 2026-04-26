async function run() {

    const text = document.getElementById("input").value;

    document.getElementById("output").innerText = "Running...";

    const res = await fetch("/run", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            input: text
        })
    });

    const data = await res.json();

    document.getElementById("output").innerText =
        JSON.stringify(data, null, 2);
}
