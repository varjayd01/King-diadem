const API_KEY = "ใส่ api_key";

async function send(){

const input=document.getElementById("msg")
const chat=document.getElementById("chat")

const msg=input.value.trim()
if(!msg)return

chat.innerHTML+=`<div class="user">🧑 ${msg}</div>`
input.value=""

const res=await fetch("/decision",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
api_key:API_KEY,
question:msg
})
})

const data=await res.json()
const r=data.reply

chat.innerHTML+=`
<div class="bot">
👑 ${r.text}<br>
⚖️ risk: ${r.risk}<br>
🧭 ${r.choices.join(", ")}
</div>
`

// 🔥 connect visualization
updateBrain(r.risk)

chat.scrollTop=chat.scrollHeight
}
