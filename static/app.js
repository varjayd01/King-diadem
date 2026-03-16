async function ask(){

let q=document.getElementById("question").value

let res=await fetch("/ask",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
question:q
})
})

let data=await res.json()

document.getElementById("response").innerText=data.answer

}

async function send(){

let name=document.getElementById("name").value
let message=document.getElementById("message").value

await fetch("/world/chat",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
name:name,
message:message
})
})

loadMessages()

}

async function loadMessages(){

let res=await fetch("/world/messages")
let data=await res.json()

let html=""

data.messages.forEach(m=>{
html+=`<p><b>${m.name}</b>: ${m.message}</p>`
})

document.getElementById("messages").innerHTML=html

}

async function upgrade(){

let res=await fetch("/create-checkout-session",{
method:"POST"
})

let data=await res.json()

window.location=data.url

}

loadMessages()
