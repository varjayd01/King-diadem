let currentChatId = null;
let chatsCache = [];
let typingEl = null;

const chatBox = () => document.getElementById("chatBox");
const chatList = () => document.getElementById("chatList");
const chatTitle = () => document.getElementById("chatTitle");
const inputEl = () => document.getElementById("input");
const newChatBtn = () => document.getElementById("newChatBtn");
const sendBtn = () => document.getElementById("sendBtn");

window.addEventListener("load", init);

async function init() {
  bindUI();
  await refreshChats();

  if (!chatsCache.length) {
    await createChat();
  } else {
    await openChat(chatsCache[0].id);
  }

  focusInput();
}

function bindUI() {
  newChatBtn().addEventListener("click", createChat);
  sendBtn().addEventListener("click", send);

  inputEl().addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  });

  inputEl().addEventListener("input", autosizeInput);
  autosizeInput();
}

function autosizeInput() {
  const el = inputEl();
  el.style.height = "auto";
  el.style.height = Math.min(el.scrollHeight, 180) + "px";
}

function focusInput() {
  setTimeout(() => inputEl().focus(), 50);
}

async function refreshChats() {
  try {
    const res = await fetch("/chats");
    const data = await res.json();
    chatsCache = data.chats || [];
    renderChatList();
  } catch (err) {
    console.error("refreshChats failed:", err);
  }
}

function renderChatList() {
  const list = chatList();
  list.innerHTML = "";

  chatsCache.forEach((chat) => {
    const item = document.createElement("div");
    item.className = "chat-item" + (chat.id === currentChatId ? " active" : "");

    const title = document.createElement("div");
    title.className = "chat-item-title";
    title.textContent = chat.title || "New Chat";

    const preview = document.createElement("div");
    preview.className = "chat-item-preview";
    preview.textContent = chat.preview || "ยังไม่มีข้อความ";

    const meta = document.createElement("div");
    meta.className = "chat-item-meta";

    const time = document.createElement("span");
    time.textContent = formatChatTime(chat.updated_at);

    const count = document.createElement("span");
    count.textContent = `${chat.count || 0} msg`;

    const del = document.createElement("button");
    del.className = "chat-delete";
    del.textContent = "×";
    del.title = "Delete chat";
    del.addEventListener("click", async (e) => {
      e.stopPropagation();
      await deleteChat(chat.id);
    });

    meta.appendChild(time);
    meta.appendChild(count);
    meta.appendChild(del);

    item.appendChild(title);
    item.appendChild(preview);
    item.appendChild(meta);

    item.addEventListener("click", () => openChat(chat.id));

    list.appendChild(item);
  });
}

function formatChatTime(iso) {
  try {
    const d = new Date(iso);
    return d.toLocaleDateString("th-TH", {
      day: "2-digit",
      month: "short",
    });
  } catch {
    return "";
  }
}

function formatMessageTime(iso) {
  try {
    const d = new Date(iso);
    return d.toLocaleString("th-TH", {
      dateStyle: "medium",
      timeStyle: "short",
    });
  } catch {
    return iso || "";
  }
}

async function createChat() {
  try {
    const res = await fetch("/new_chat", { method: "POST" });
    const data = await res.json();

    currentChatId = data.chat_id;
    chatTitle().textContent = data.title || "New Chat";
    chatBox().innerHTML = "";

    await refreshChats();
    highlightCurrentChat();
    focusInput();
  } catch (err) {
    console.error("createChat failed:", err);
  }
}

async function openChat(id) {
  try {
    currentChatId = id;

    const res = await fetch(`/chat/${id}`);
    const data = await res.json();
    const chat = data.chat || {};

    chatTitle().textContent = chat.title || "New Chat";
    renderMessages(chat.messages || []);
    highlightCurrentChat();
    focusInput();
  } catch (err) {
    console.error("openChat failed:", err);
  }
}

function renderMessages(messages) {
  const box = chatBox();
  box.innerHTML = "";

  if (!messages.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.innerHTML = `
      <div>พิมพ์มาได้เลยค่ะ</div>
      <div>กดค้างที่ข้อความเพื่อดูเวลา</div>
    `;
    box.appendChild(empty);
    return;
  }

  messages.forEach((m) => {
    appendMessage(m.role, m.content, m.timestamp, false);
  });

  scrollToBottom();
}

function appendMessage(role, content, timestamp, shouldScroll = true) {
  const box = chatBox();

  const message = document.createElement("div");
  message.className = `message ${role === "user" ? "user" : "assistant"}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = content;

  const meta = document.createElement("div");
  meta.className = "timestamp";
  meta.textContent = formatMessageTime(timestamp);

  message.appendChild(bubble);
  message.appendChild(meta);

  attachLongPress(message);

  box.appendChild(message);

  if (shouldScroll) scrollToBottom();
  return message;
}

function attachLongPress(el) {
  let timer = null;
  let revealed = false;

  const start = () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      el.classList.add("revealed");
      revealed = true;
    }, 450);
  };

  const stop = () => {
    clearTimeout(timer);
    if (revealed) {
      el.classList.remove("revealed");
      revealed = false;
    }
  };

  el.addEventListener("pointerdown", start);
  el.addEventListener("pointerup", stop);
  el.addEventListener("pointercancel", stop);
  el.addEventListener("pointerleave", stop);
  el.addEventListener("contextmenu", (e) => e.preventDefault());
}

function scrollToBottom() {
  const box = chatBox();
  box.scrollTop = box.scrollHeight;
}

function showTyping() {
  hideTyping();

  typingEl = document.createElement("div");
  typingEl.className = "typing";
  typingEl.innerHTML = "<span></span><span></span><span></span>";
  chatBox().appendChild(typingEl);
  scrollToBottom();
}

function hideTyping() {
  if (typingEl && typingEl.parentNode) {
    typingEl.parentNode.removeChild(typingEl);
  }
  typingEl = null;
}

async function send() {
  const input = inputEl();
  const text = input.value.trim();

  if (!text || !currentChatId) return;

  const localTime = new Date().toISOString();
  appendMessage("user", text, localTime);

  input.value = "";
  autosizeInput();
  showTyping();

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: currentChatId,
        question: text,
      }),
    });

    const data = await res.json();
    hideTyping();

    appendMessage("assistant", data.answer || "ไม่มีคำตอบ", data.timestamp || new Date().toISOString());
    chatTitle().textContent = data.title || chatTitle().textContent;

    await refreshChats();
    highlightCurrentChat();
  } catch (err) {
    hideTyping();
    console.error("send failed:", err);
    appendMessage("assistant", "❌ ระบบตอบไม่ได้ตอนนี้ แต่แชทยังไม่พังค่ะ", new Date().toISOString());
  }

  focusInput();
}

async function deleteChat(id) {
  try {
    await fetch(`/chat/${id}`, { method: "DELETE" });

    if (currentChatId === id) {
      currentChatId = null;
      chatBox().innerHTML = "";
      chatTitle().textContent = "New Chat";
    }

    await refreshChats();

    if (!currentChatId && chatsCache.length) {
      await openChat(chatsCache[0].id);
    } else if (!chatsCache.length) {
      await createChat();
    }
  } catch (err) {
    console.error("deleteChat failed:", err);
  }
}

function highlightCurrentChat() {
  document.querySelectorAll(".chat-item").forEach((el) => {
    el.classList.remove("active");
  });

  const items = [...document.querySelectorAll(".chat-item")];
  const active = items.find((el, idx) => chatsCache[idx] && chatsCache[idx].id === currentChatId);

  if (active) active.classList.add("active");
}
