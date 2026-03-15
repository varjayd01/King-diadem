const canvas = document.getElementById("galaxy")
const ctx = canvas.getContext("2d")

let nodes = [

{ x:300, y:200, name:"AI CORE"},
{ x:500, y:350, name:"DECISION"},
{ x:700, y:200, name:"SIMULATION"}

]

function drawNodes(){

ctx.fillStyle="cyan"

nodes.forEach(n=>{

ctx.beginPath()

ctx.arc(n.x,n.y,6,0,Math.PI*2)

ctx.fill()

})

}
