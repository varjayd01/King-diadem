async function send(){
    const msg = document.getElementById("msg").value
    const chat = document.getElementById("chat")

    chat.innerHTML += `<div class="msg user">YOU: ${msg}</div>`

    const res = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: msg,
            location: "unknown",
            food: 0,
            money: 0,
            risk: 0
        })
    })

    const data = await res.json()

    chat.innerHTML += `<div class="msg ai">AI: ${data.reply}</div>`

    document.getElementById("msg").value = ""
    chat.scrollTop = chat.scrollHeight
}
