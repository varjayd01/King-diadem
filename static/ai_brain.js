// static/ai_brain.js
(function () {
  const canvas = document.getElementById("brain");
  if (!canvas) return;

  const ctx = window.KD.resizeCanvas(canvas);
  const nodes = Array.from({ length: 28 }, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    vx: (Math.random() - 0.5) * 0.7,
    vy: (Math.random() - 0.5) * 0.7,
  }));

  function loop() {
    const risk = Number(window.KD.state?.risk?.risk_score ?? 0);
    const pulse = Math.max(0.5, 1 + risk / 100);

    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);

    nodes.forEach((n) => {
      n.x += n.vx * pulse;
      n.y += n.vy * pulse;

      if (n.x < 0 || n.x > window.innerWidth) n.vx *= -1;
      if (n.y < 0 || n.y > window.innerHeight) n.vy *= -1;

      ctx.beginPath();
      ctx.arc(n.x, n.y, 2.4, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(120,240,255,0.95)";
      ctx.fill();
    });

    nodes.forEach((a, i) => {
      for (let j = i + 1; j < nodes.length; j++) {
        const b = nodes[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 140) {
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = `rgba(90,200,255,${0.18 - dist / 1200})`;
          ctx.stroke();
        }
      }
    });

    requestAnimationFrame(loop);
  }

  window.addEventListener("resize", () => window.KD.resizeCanvas(canvas));
  loop();
})();
