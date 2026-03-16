const canvas=document.getElementById("orbit")
const ctx=canvas.getContext("2d")

let particles=[]

for(let i=0;i<60;i++){

particles.push({

angle:Math.random()*360,
distance:50+Math.random()*150

})

}

function animate(){

ctx.clearRect(0,0,canvas.width,canvas.height)

let cx=canvas.width/2
let cy=canvas.height/2

particles.forEach(p=>{

p.angle+=0.5

let rad=p.angle*Math.PI/180

let x=cx+Math.cos(rad)*p.distance
let y=cy+Math.sin(rad)*p.distance

ctx.beginPath()
ctx.arc(x,y,2,0,Math.PI*2)
ctx.fillStyle="#00ffff"
ctx.fill()

})

requestAnimationFrame(animate)

}

animate()
