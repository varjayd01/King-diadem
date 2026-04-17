// static/galaxy.js
(function () {
  const canvas = document.getElementById("galaxy");
  if (!canvas) return;

  const ctx = window.KD.resizeCanvas(canvas);

  const nodes = [
    { x: 300, y: 230, name: "AI CORE" },
    { x: 540, y: 300, name: "DECISION" },
    { x: 760, y: 210, name: "SIMULATION" },
    { x: 480, y: 150, name: "GOVERNANCE" },
  ];

  function draw() {
    const risk = Number(window.KD.state?.risk?.risk_score ?? 0);
    const alpha = 0.15 + risk / 600;

    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);

    nodes.forEach((n) => {
      ctx.beginPath();
      ctx.arc(n.x, n.y, 12, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(100,255,255,0.8)";
      ctx.fill();

      ctx.fillStyle = "rgba(230,250,255,0.85)";
      ctx.font = "12px monospace";
      ctx.fillText(n.name, n.x + 18, n.y + 4);
    });

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i];
        const b = nodes[j];
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = `rgba(80,200,255,${alpha})`;
        ctx.stroke();
      }
    }

    requestAnimationFrame(draw);
  }

  window.addEventListener("resize", () => window.KD.resizeCanvas(canvas));
  draw();
})();
