const canvas = document.getElementById("thinkingOrbit")
const ctx = canvas.getContext("2d")

canvas.width = window.innerWidth
canvas.height = 300

let dots=[]

for(let i=0;i<40;i++){

dots.push({

x:Math.random()*canvas.width,
y:Math.random()*canvas.height,
vx:(Math.random()-0.5)*0.5,
vy:(Math.random()-0.5)*0.5

})

}

function animate(){

ctx.clearRect(0,0,canvas.width,canvas.height)

dots.forEach(d=>{

d.x+=d.vx
d.y+=d.vy

if(d.x<0||d.x>canvas.width)d.vx*=-1
if(d.y<0||d.y>canvas.height)d.vy*=-1

ctx.beginPath()
ctx.arc(d.x,d.y,2,0,Math.PI*2)
ctx.fillStyle="#66ccff"
ctx.fill()

})

requestAnimationFrame(animate)

}

animate()
