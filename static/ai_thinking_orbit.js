const canvas = document.getElementById("thinkingOrbit")
if (!canvas) {
  console.warn("thinkingOrbit canvas not found")
}

const ctx = canvas?.getContext("2d")

function resize(){
  canvas.width = window.innerWidth
  canvas.height = 300
}
resize()
window.addEventListener("resize", resize)

let dots = []

// 🔹 init
for(let i=0;i<40;i++){
  dots.push(createDot())
}

function createDot(x=null,y=null){
  return {
    x: x ?? Math.random()*canvas.width,
    y: y ?? Math.random()*canvas.height,
    vx:(Math.random()-0.5)*0.5,
    vy:(Math.random()-0.5)*0.5
  }
}

// 🧠 จุดศูนย์กลาง
function getCenter(){
  return {
    x: canvas.width/2,
    y: canvas.height/2
  }
}

// 🔥 inject จากระบบ (สำคัญ)
window.injectThought = function(text){
  const c = getCenter()

  dots.push({
    x: c.x,
    y: c.y,
    vx:(Math.random()-0.5)*2,
    vy:(Math.random()-0.5)*2,
    text: text
  })
}

// 🌌 animate
function animate(){

  if(!ctx) return

  ctx.clearRect(0,0,canvas.width,canvas.height)

  const center = getCenter()

  // 🔹 update dots
  dots.forEach(d=>{

    let dx = center.x - d.x
    let dy = center.y - d.y
    let dist = Math.sqrt(dx*dx + dy*dy) || 1

    let force = 0.0005

    d.vx += dx * force
    d.vy += dy * force

    d.x += d.vx
    d.y += d.vy

    ctx.beginPath()
    ctx.arc(d.x,d.y,2,0,Math.PI*2)
    ctx.fillStyle="#66ccff"
    ctx.fill()

  })

  // 🔗 connection
  for(let i=0;i<dots.length;i++){
    for(let j=i+1;j<dots.length;j++){

      let dx = dots[i].x - dots[j].x
      let dy = dots[i].y - dots[j].y
      let dist = Math.sqrt(dx*dx + dy*dy)

      if(dist < 100){
        ctx.beginPath()
        ctx.moveTo(dots[i].x, dots[i].y)
        ctx.lineTo(dots[j].x, dots[j].y)
        ctx.strokeStyle="rgba(102,204,255,0.15)"
        ctx.stroke()
      }

    }
  }

  requestAnimationFrame(animate)
}

animate()
