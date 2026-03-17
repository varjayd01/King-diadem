/* 🧠 ASK SYSTEM */
async function ask(){

let q=document.getElementById("question").value

if(!q){
return
}

let thinking=document.getElementById("thinking")

let dots=0

let interval=setInterval(()=>{
dots++
thinking.innerText="AI thinking"+".".repeat(dots%4)
},300)

try{

let res=await fetch("/ask",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({question:q})
})

let data=await res.json()

clearInterval(interval)

thinking.innerText=""

document.getElementById("response").innerText=data.answer

}catch(e){

clearInterval(interval)

thinking.innerText=""

document.getElementById("response").innerText="System error. Try again."

}

}


/* 🌌 GALAXY ORBIT (ลื่นขึ้น) */
let canvas=document.getElementById("galaxy")
let ctx=canvas.getContext("2d")

let nodes=[]

for(let i=0;i<30;i++){
nodes.push({
angle:Math.random()*Math.PI*2,
radius:60+Math.random()*120,
speed:0.002+Math.random()*0.004
})
}

function draw(){

ctx.clearRect(0,0,400,400)

let cx=200
let cy=200

nodes.forEach(n=>{

n.angle+=n.speed

let x=cx+Math.cos(n.angle)*n.radius
let y=cy+Math.sin(n.angle)*n.radius

ctx.beginPath()
ctx.arc(x,y,2,0,Math.PI*2)
ctx.fillStyle="#ffffff"
ctx.fill()

})

requestAnimationFrame(draw)
}

draw()


/* 🌍 GLOBAL SIGNAL */
function updateSignal(){

let value=Math.random()*100

document.getElementById("signalFill").style.width=value+"%"

if(value<40){
document.getElementById("signalText").innerText="Human pressure increasing"
}else if(value<70){
document.getElementById("signalText").innerText="System stabilizing"
}else{
document.getElementById("signalText").innerText="Choices expanding"
}

}

setInterval(updateSignal,3000)
