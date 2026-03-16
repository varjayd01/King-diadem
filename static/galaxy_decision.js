const canvas = document.getElementById("galaxyDecision")
const ctx = canvas.getContext("2d")

canvas.width = window.innerWidth
canvas.height = window.innerHeight

let nodes = []

function drawGalaxy(problem, paths){

nodes = []

let centerX = canvas.width/2
let centerY = canvas.height/2

nodes.push({
name:problem,
x:centerX,
y:centerY,
type:"core"
})

let radius = 220

paths.forEach((p,i)=>{

let angle = (i/paths.length) * Math.PI * 2

let x = centerX + Math.cos(angle) * radius
let y = centerY + Math.sin(angle) * radius

nodes.push({
name:p.strategy,
x:x,
y:y,
risk:p.risk,
confidence:p.confidence
})

})

render()

}

function render(){

ctx.clearRect(0,0,canvas.width,canvas.height)

nodes.forEach((n,i)=>{

ctx.beginPath()

ctx.arc(n.x,n.y,10,0,Math.PI*2)

ctx.fillStyle = i===0 ? "#ffd700" : "#66ccff"

ctx.fill()

ctx.fillStyle="white"

ctx.fillText(n.name,n.x+14,n.y)

})

}
