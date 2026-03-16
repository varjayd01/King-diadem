const canvas=document.getElementById("galaxy")

const ctx=canvas.getContext("2d")

canvas.width=window.innerWidth

canvas.height=window.innerHeight

const stars=[]

const members=[

"Altair","Vega","Lyla",

"Titan","FATE","DriftZero"

]

members.forEach(m=>{

stars.push({

name:m,

angle:Math.random()*360,

distance:200+Math.random()*80

})

})

function draw(){

ctx.clearRect(0,0,canvas.width,canvas.height)

let cx=canvas.width/2

let cy=canvas.height/2

stars.forEach(s=>{

s.angle+=0.1

let rad=s.angle*Math.PI/180

let x=cx+Math.cos(rad)*s.distance

let y=cy+Math.sin(rad)*s.distance

ctx.beginPath()

ctx.arc(x,y,6,0,Math.PI*2)

ctx.fillStyle="white"

ctx.fill()

ctx.fillText(s.name,x+10,y)

})

requestAnimationFrame(draw)

}

draw()
