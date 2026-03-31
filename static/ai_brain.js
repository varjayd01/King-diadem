const brain=document.getElementById("brain")

const ctx=brain.getContext("2d")

brain.width=window.innerWidth
brain.height=window.innerHeight


let nodes=[]

for(let i=0;i<30;i++){

nodes.push({

x:Math.random()*brain.width,

y:Math.random()*brain.height,

vx:(Math.random()-0.5)*0.6,

vy:(Math.random()-0.5)*0.6

})

}



function brainLoop(){

ctx.clearRect(0,0,brain.width,brain.height)

nodes.forEach(n=>{

n.x+=n.vx

n.y+=n.vy

if(n.x<0||n.x>brain.width) n.vx*=-1
if(n.y<0||n.y>brain.height) n.vy*=-1


ctx.beginPath()

ctx.arc(n.x,n.y,2,0,Math.PI*2)

ctx.fillStyle="#4fd1ff"

ctx.fill()



nodes.forEach(n2=>{

let dx=n.x-n2.x

let dy=n.y-n2.y

let dist=Math.sqrt(dx*dx+dy*dy)


if(dist<140){

ctx.beginPath()

ctx.moveTo(n.x,n.y)

ctx.lineTo(n2.x,n2.y)

ctx.strokeStyle="rgba(79,209,255,0.15)"

ctx.stroke()

}

})

})

requestAnimationFrame(brainLoop)

}

brainLoop()
