// =======================================
// KING DIADEM GLOBAL ENGINE
// =======================================

// -----------------------------
// JARVIS THINKING
// -----------------------------

let thinkingTimer

function startThinking(){

let r=document.getElementById("response")
let dots=0

thinkingTimer=setInterval(()=>{

dots++
r.innerText="AI Council thinking"+".".repeat(dots%4)

},350)

}

function stopThinking(){

clearInterval(thinkingTimer)

}


// -----------------------------
// ASK AI
// -----------------------------

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


// -----------------------------
// GLOBAL CHAT
// -----------------------------

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


// -----------------------------
// STRIPE UPGRADE
// -----------------------------

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


// =======================================
// GALAXY DECISION MAP
// =======================================

const galaxy=document.getElementById("galaxy")

if(galaxy){

const ctx=galaxy.getContext("2d")

galaxy.width=window.innerWidth
galaxy.height=420

let nodes=[]

for(let i=0;i<90;i++){

nodes.push({

x:Math.random()*galaxy.width,
y:Math.random()*galaxy.height,
vx:(Math.random()-0.5)*0.4,
vy:(Math.random()-0.5)*0.4

})

}

function drawGalaxy(){

ctx.clearRect(0,0,galaxy.width,galaxy.height)

nodes.forEach(n=>{

n.x+=n.vx
n.y+=n.vy

if(n.x<0||n.x>galaxy.width)n.vx*=-1
if(n.y<0||n.y>galaxy.height)n.vy*=-1

ctx.beginPath()
ctx.arc(n.x,n.y,2,0,Math.PI*2)
ctx.fillStyle="#7a95ff"
ctx.fill()

})

requestAnimationFrame(drawGalaxy)

}

drawGalaxy()

}


// =======================================
// PLANETARY SIGNAL MONITOR
// =======================================

function planetarySignal(){

let pressure=Math.random()

if(pressure>0.8){

console.log("Planetary pressure rising")

}

if(pressure<0.2){

console.log("Planetary stability")

}

}

setInterval(planetarySignal,10000)


// =======================================
// GLOBAL DECISION HEATMAP
// =======================================

function generateDecisionMap(problem){

let options=[

"observe situation",
"gather more information",
"execute limited action",
"collaborate with others"

]

return options

}


// =======================================
// CIVILIZATION SIGNAL
// =======================================

function civilizationSignal(){

let signal=Math.random()

if(signal>0.7){

console.log("Human choice expanding")

}

else{

console.log("Human pressure increasing")

}

}

setInterval(civilizationSignal,15000)
