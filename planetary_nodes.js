const nodeCanvas=document.getElementById("nodes")

const ctx=nodeCanvas.getContext("2d")

nodeCanvas.width=window.innerWidth
nodeCanvas.height=window.innerHeight

let nodes=[]

for(let i=0;i<25;i++){

nodes.push({

x:Math.random()*nodeCanvas.width,
y:Math.random()*nodeCanvas.height

})

}

function drawNodes(){

ctx.clearRect(0,0,nodeCanvas.width,nodeCanvas.height)

nodes.forEach(n=>{

ctx.beginPath()
ctx.arc(n.x,n.y,3,0,Math.PI*2)
ctx.fillStyle="#4fd1ff"
ctx.fill()

nodes.forEach(n2=>{

let dx=n.x-n2.x
let dy=n.y-n2.y
let dist=Math.sqrt(dx*dx+dy*dy)

if(dist<180){

ctx.beginPath()
ctx.moveTo(n.x,n.y)
ctx.lineTo(n2.x,n2.y)
ctx.strokeStyle="rgba(79,209,255,0.12)"
ctx.stroke()

}

})

})

requestAnimationFrame(drawNodes)

}

drawNodes()
