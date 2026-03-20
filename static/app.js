console.log("APP LOADED V3")

let chat_id = null

window.onload = async () => {
    document.getElementById("newChatBtn").onclick = createChat
    document.getElementById("sendBtn").onclick = send

    await createChat()
}

async function createChat() {
    const res = await fetch('/new_chat', { method: 'POST' })
    const data = await res.json()

    chat_id = data.chat_id

    document.getElementById("chatBox").innerHTML = ""
}

async function send() {
    const input = document.getElementById("input")
    const text = input.value

    if (!text) return

    add("user", text)

    const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: text, chat_id })
    })

    const data = await res.json()

    add("ai", data.answer)

    input.value = ""
}

function add(role, text) {
    const box = document.getElementById("chatBox")

    const div = document.createElement("div")
    div.innerText = text
    div.className = role

    box.appendChild(div)
}
