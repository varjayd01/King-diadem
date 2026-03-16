// ==========================
// KING DIADEM APP ENGINE
// ==========================

let thinkingInterval

// ==========================
// ASK AI
// ==========================

async function ask(){

let q=document.getElementById("question").value

startThinking()

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

stopThinking()

document.getElementById("response").innerText=data.answer

}


// ==========================
// JARVIS THINKING
// ==========================

function startThinking(){

let r=document.getElementById("response")

let dots=0

thinkingInterval=setInterval(()=>{

dots++

r.innerText="AI Council thinking"+".".repeat(dots%4)

},400)

}

function stopThinking(){

clearInterval(thinkingInterval)

}


// ==========================
// GLOBAL CHAT
// ==========================

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

loadMessages()


// ==========================
// STRIPE UPGRADE
// ==========================

async function upgrade(plan){

let res=await fetch("/create-checkout-session",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
plan:plan
})

})

let data=await res.json()

window.location=data.url

}


// ==========================
// GALAXY DECISION MAP
// ==========================

const canvas=document.getElementById("galaxy")

if(canvas){

const ctx=canvas.getContext("2d")

canvas.width=window.innerWidth
canvas.height=400

let nodes=[]

for(let i=0;i<60;i++){

nodes.push({
x:Math.random()*canvas.width,
y:Math.random()*canvas.height,
vx:(Math.random()-0.5)*0.4,
vy:(Math.random()-0.5)*0.4
})

}

function draw(){

ctx.clearRect(0,0,canvas.width,canvas.height)

nodes.forEach(n=>{

n.x+=n.vx
n.y+=n.vy

if(n.x<0||n.x>canvas.width)n.vx*=-1
if(n.y<0||n.y>canvas.height)n.vy*=-1

ctx.beginPath()
ctx.arc(n.x,n.y,2,0,Math.PI*2)
ctx.fillStyle="#7a95ff"
ctx.fill()

})

requestAnimationFrame(draw)

}

draw()

}


// ==========================
// PLANETARY SIGNAL
// ==========================

function planetarySignal(){

let signal=Math.random()

if(signal>0.7){

console.log("Global pressure rising")

}

}

setInterval(planetarySignal,10000)


// ==========================
// DECISION TREE GENERATOR
// ==========================

function generateDecisionTree(problem){

let options=[

"Gather more information",
"Delay decision",
"Execute controlled action",
"Seek collaboration"

]

return options

}
