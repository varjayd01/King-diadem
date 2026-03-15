const canvas=document.getElementById("universe")

const ctx=canvas.getContext("2d")

canvas.width=window.innerWidth
canvas.height=window.innerHeight


let stars=[]

for(let i=0;i<150;i++){

stars.push({

x:Math.random()*canvas.width,

y:Math.random()*canvas.height,

size:Math.random()*2

})

}


function drawUniverse(){

ctx.clearRect(0,0,canvas.width,canvas.height)

stars.forEach(s=>{

ctx.beginPath()

ctx.arc(s.x,s.y,s.size,0,Math.PI*2)

ctx.fillStyle="#ffffff"

ctx.fill()

})

requestAnimationFrame(drawUniverse)

}

drawUniverse()
