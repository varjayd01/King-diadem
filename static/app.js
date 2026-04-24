async function run() {

    const text = document.getElementById("input").value;

    const res = await fetch("/run", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text
        })
    });

    const data = await res.json();

    document.getElementById("output").innerText =
        JSON.stringify(data, null, 2);
}
