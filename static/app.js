const chat = document.getElementById("chat");

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = "message " + type;
  div.innerText = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function run() {
  const input = document.getElementById("input");
  const text = input.value.trim();
  if (!text) return;

  addMessage("👤 " + text, "user");
  input.value = "";

  try {
    const res = await fetch("/decision", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();

    addMessage("🤖 " + data.response, "ai");

  } catch (err) {
    addMessage("❌ ระบบมีปัญหา", "ai");
  }
}

function stop() {
  addMessage("⛔ STOPPED", "ai");
}
