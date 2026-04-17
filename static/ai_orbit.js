// static/ai_orbit.js
(function () {
  const canvas = document.getElementById("orbit");
  if (!canvas) return;

  const ctx = window.KD.resizeCanvas(canvas);

  const particles = [];
  for (let i = 0; i < 60; i++) {
    particles.push({
      angle: Math.random() * Math.PI * 2,
      distance: 60 + Math.random() * 220,
      speed: 0.004 + Math.random() * 0.01,
      size: 1 + Math.random() * 2.3,
    });
  }

  function animate() {
    const confidence = Number(window.KD.state?.consensus?.confidence ?? 50);
    const speedBoost = Math.max(0.5, confidence / 40);

    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
    const cx = window.innerWidth / 2;
    const cy = window.innerHeight / 2;

    particles.forEach((p) => {
      p.angle += p.speed * speedBoost;

      const x = cx + Math.cos(p.angle) * p.distance;
      const y = cy + Math.sin(p.angle) * p.distance;

      ctx.beginPath();
      ctx.arc(x, y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(100,255,220,0.7)";
      ctx.fill();
    });

    requestAnimationFrame(animate);
  }

  window.addEventListener("resize", () => window.KD.resizeCanvas(canvas));
  animate();
})();
