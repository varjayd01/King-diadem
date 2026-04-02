// ===== API =====
async function run() {
    const msg = document.getElementById("msg").value;

    const res = await fetch("/brain", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text: msg })
    });

    const data = await res.json();

    document.getElementById("out").innerText =
        JSON.stringify(data, null, 2);
}

// ===== SPACE ANIMATION =====
const canvas = document.getElementById("bg");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let angle = 0;

function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);

    // sun
    ctx.fillStyle = "yellow";
    ctx.beginPath();
    ctx.arc(canvas.width/2, canvas.height/2, 20, 0, Math.PI*2);
    ctx.fill();

    // earth orbit
    let x = canvas.width/2 + Math.cos(angle) * 150;
    let y = canvas.height/2 + Math.sin(angle) * 150;

    ctx.fillStyle = "blue";
    ctx.beginPath();
    ctx.arc(x, y, 10, 0, Math.PI*2);
    ctx.fill();

    angle += 0.01;
    requestAnimationFrame(draw);
}

draw();
