async function send() {
    const input = document.getElementById("input");
    const chat = document.getElementById("chat");
    const mode = document.getElementById("mode").value;

    const text = input.value;

    chat.innerHTML += `<div class="bubble user">${text}</div>`;

    const res = await fetch("/decision", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            input: text,
            mode: mode
        })
    });

    const data = await res.json();

    chat.innerHTML += `<div class="bubble ai">${data.result}</div>`;

    input.value = "";
}
