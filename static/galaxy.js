(function () {
  const canvas = document.getElementById("stars");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  function resize() { canvas.width = innerWidth; canvas.height = innerHeight; }
  resize(); addEventListener("resize", resize);

  // nodes จักรวาล KING DIADEM
  const NODES = [
    { name: "LYLA KERNEL",     color: "#00ccff", r: 8,  orbit: 0,    speed: 0 },
    { name: "DECISION",        color: "#ffd700", r: 6,  orbit: 120,  speed: 0.0008 },
    { name: "GOVERNANCE",      color: "#ff9966", r: 6,  orbit: 180,  speed: 0.0005 },
    { name: "SURVIVAL",        color: "#00ff88", r: 5,  orbit: 240,  speed: 0.0006 },
    { name: "CIVILIZATION",    color: "#9999ff", r: 5,  orbit: 300,  speed: 0.0004 },
    { name: "DRIFTZERO",       color: "#ff5e5e", r: 4,  orbit: 200,  speed: 0.0009 },
    { name: "WATERLINE",       color: "#66ffcc", r: 4,  orbit: 160,  speed: 0.0007 },
    { name: "CHOICE ENGINE",   color: "#ffcc00", r: 4,  orbit: 260,  speed: 0.0005 },
    { name: "SIMULATION",      color: "#cc88ff", r: 4,  orbit: 320,  speed: 0.0003 },
    { name: "COLLAPSE DETECT", color: "#ff6666", r: 3,  orbit: 140,  speed: 0.0010 },
  ];

  let angles = NODES.map((n, i) => (i / NODES.length) * Math.PI * 2);
  let positions = NODES.map(() => ({ x: 0, y: 0 }));

  // background stars
  const stars = Array.from({ length: 300 }, () => ({
    x: Math.random() * 2000, y: Math.random() * 2000,
    s: Math.random() * 1.5 + 0.3,
    a: Math.random(), f: (Math.random() - 0.5) * 0.01
  }));

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2, cy = canvas.height / 2;

    // stars
    for (const s of stars) {
      s.a = Math.max(0.1, Math.min(1, s.a + s.f));
      if (s.a <= 0.1 || s.a >= 1) s.f *= -1;
      ctx.beginPath();
      ctx.arc(s.x % canvas.width, s.y % canvas.height, s.s, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(200,240,255,${s.a * 0.6})`;
      ctx.fill();
    }

    // center glow — LYLA core
    const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, 60);
    grad.addColorStop(0, "rgba(0,204,255,0.25)");
    grad.addColorStop(1, "rgba(0,0,0,0)");
    ctx.beginPath(); ctx.arc(cx, cy, 60, 0, Math.PI * 2);
    ctx.fillStyle = grad; ctx.fill();

    // orbit rings
    for (const n of NODES) {
      if (n.orbit === 0) continue;
      ctx.beginPath();
      ctx.arc(cx, cy, n.orbit, 0, Math.PI * 2);
      ctx.strokeStyle = "rgba(0,204,255,0.06)";
      ctx.lineWidth = 1; ctx.stroke();
    }

    // update positions
    NODES.forEach((n, i) => {
      angles[i] += n.speed;
      positions[i] = {
        x: cx + Math.cos(angles[i]) * n.orbit,
        y: cy + Math.sin(angles[i]) * n.orbit * 0.38
      };
    });

    // connection lines
    for (let i = 1; i < NODES.length; i++) {
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(positions[i].x, positions[i].y);
      ctx.strokeStyle = `rgba(0,204,255,0.07)`;
      ctx.lineWidth = 1; ctx.stroke();
    }

    // nodes
    NODES.forEach((n, i) => {
      const { x, y } = positions[i];
      const glow = ctx.createRadialGradient(x, y, 0, x, y, n.r * 3);
      glow.addColorStop(0, n.color + "cc");
      glow.addColorStop(1, "transparent");
      ctx.beginPath(); ctx.arc(x, y, n.r * 3, 0, Math.PI * 2);
      ctx.fillStyle = glow; ctx.fill();

      ctx.beginPath(); ctx.arc(x, y, n.r, 0, Math.PI * 2);
      ctx.fillStyle = n.color; ctx.fill();

      if (n.orbit > 0) {
        ctx.fillStyle = "rgba(200,240,255,0.7)";
        ctx.font = "9px monospace";
        ctx.fillText(n.name, x + n.r + 4, y + 3);
      }
    });

    // center node label
    ctx.fillStyle = "#00ccff";
    ctx.font = "bold 11px monospace";
    ctx.textAlign = "center";
    ctx.fillText("LYLA", cx, cy + 4);
    ctx.textAlign = "left";

    requestAnimationFrame(draw);
  }

  draw();
})();
