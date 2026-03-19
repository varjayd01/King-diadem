let chat_id = null
let chats = []

// ---------------- INIT ----------------
window.onload = async () => {
    chats = JSON.parse(localStorage.getItem("chats") || "[]")

    if (chats.length === 0) {
        await createChat()
    } else {
        chat_id = chats[0]
        loadHistory()
    }

    renderChatList()
}

// ---------------- CREATE CHAT ----------------
async function createChat() {
    const res = await fetch('/new_chat', { method: 'POST' })
    const data = await res.json()

    chat_id = data.chat_id

    chats.unshift(chat_id)
    localStorage.setItem("chats", JSON.stringify(chats))

    document.getElementById("chatBox").innerHTML = ""

    renderChatList()
}

// ---------------- SWITCH CHAT ----------------
function switchChat(id) {
    chat_id = id
    loadHistory()
}

// ---------------- RENDER SIDEBAR ----------------
function renderChatList() {
    const list = document.getElementById("chatList")
    list.innerHTML = ""

    chats.forEach(id => {
        const div = document.createElement("div")
        div.innerText = "Chat " + id.slice(0, 4)
        div.onclick = () => switchChat(id)
        list.appendChild(div)
    })
}

// ---------------- LOAD HISTORY ----------------
async function loadHistory() {
    const res = await fetch(`/chat/${chat_id}`)
    const data = await res.json()

    const box = document.getElementById("chatBox")
    box.innerHTML = ""

    data.messages.forEach(m => {
        addMessage("user", m.q)
        addMessage("ai", m.a)
    })
}

// ---------------- SEND ----------------
async function send() {
    const input = document.getElementById("input")
    const text = input.value

    if (!text) return

    addMessage("user", text)

    const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            question: text,
            chat_id: chat_id
        })
    })

    const data = await res.json()

    addMessage("ai", data.answer)

    input.value = ""
}

// ---------------- 120FPS RENDER ----------------
let queue = []

function addMessage(role, text) {
    queue.push({ role, text })
}

function loop() {
    const box = document.getElementById("chatBox")

    while (queue.length > 0) {
        const { role, text } = queue.shift()

        const div = document.createElement("div")
        div.className = role
        div.innerText = text

        box.appendChild(div)
    }

    box.scrollTop = box.scrollHeight

    requestAnimationFrame(loop)
}

loop()
