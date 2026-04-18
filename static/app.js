async function send() {
    const input = document.getElementById("input").value;

    const res = await fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            input: input,
            entropy: 40,
            stability: 60
        })
    });

    const data = await res.json();

    document.getElementById("output").innerText =
        JSON.stringify(data, null, 2);
}
