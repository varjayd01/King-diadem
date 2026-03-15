const canvas=document.getElementById("universe")
const ctx=canvas.getContext("2d")

canvas.width=window.innerWidth
canvas.height=window.innerHeight

let nodes=[]

for(let i=0;i<80;i++){

nodes.push({

x:Math.random()*canvas.width,
y:Math.random()*canvas.height,
vx:(Math.random()-0.5)*0.3,
vy:(Math.random()-0.5)*0.3

})

}

function draw(){

ctx.clearRect(0,0,canvas.width,canvas.height)

nodes.forEach(n=>{

n.x+=n.vx
n.y+=n.vy

ctx.beginPath()
ctx.arc(n.x,n.y,2,0,Math.PI*2)
ctx.fillStyle="#6fdcff"
ctx.fill()

nodes.forEach(n2=>{

const dx=n.x-n2.x
const dy=n.y-n2.y
const dist=Math.sqrt(dx*dx+dy*dy)

if(dist<120){

ctx.beginPath()
ctx.moveTo(n.x,n.y)
ctx.lineTo(n2.x,n2.y)
ctx.strokeStyle="rgba(100,200,255,0.15)"
ctx.stroke()

}

})

})

requestAnimationFrame(draw)

}

draw()
