// static/galaxy.js — KING DIADEM Solar System
// LYLA = governance core | VEGA = explorer/simulation AI
(function () {
  const canvas = document.getElementById("galaxy-bg");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  function resize() {
    canvas.width = innerWidth;
    canvas.height = innerHeight;
  }
  resize();
  addEventListener("resize", resize);

  // ── SOLAR SYSTEM NODES ────────────────────────────────────────
  const SUN = { name: "LYLA", color: "#00d4ff", r: 10, glow: 40 };

  const PLANETS = [
    { name: "VEGA",        color: "#ffd27f", r: 6,  orbit: 90,  speed: 0.0012, angle: 0,    label: true },
    { name: "DECISION",    color: "#c8a96e", r: 4,  orbit: 140, speed: 0.0008, angle: 1.2,  label: false },
    { name: "DRIFTZERO",   color: "#ff6a00", r: 3,  orbit: 185, speed: 0.0006, angle: 2.5,  label: false },
    { name: "WATERLINE",   color: "#00ff88", r: 3,  orbit: 225, speed: 0.0005, angle: 0.8,  label: false },
    { name: "SURVIVAL",    color: "#66ffcc", r: 4,  orbit: 270, speed: 0.0004, angle: 3.1,  label: false },
    { name: "CIVILIZATION",color: "#9999ff", r: 5,  orbit: 320, speed: 0.0003, angle: 1.8,  label: true  },
    { name: "COLLAPSE",    color: "#ff5e5e", r: 2,  orbit: 155, speed: 0.0010, angle: 4.2,  label: false },
    { name: "CHOICE",      color: "#ffd700", r: 3,  orbit: 245, speed: 0.0005, angle: 5.5,  label: false },
    { name: "SUPPLY",      color: "#88ddff", r: 3,  orbit: 360, speed: 0.0002, angle: 2.2,  label: false },
  ];

  // Moons for VEGA
  const VEGA_MOONS = [
    { name: "SIM",   color: "#cc88ff", r: 2, orbit: 22, speed: 0.004, angle: 0 },
    { name: "WORLD", color: "#88ccff", r: 1.5, orbit: 32, speed: 0.003, angle: 2 },
  ];

  // ── NEBULA PARTICLES ──────────────────────────────────────────
  const NEBULA = Array.from({ length: 120 }, () => ({
    x: Math.random() * 2000 - 1000,
    y: Math.random() * 2000 - 1000,
    r: Math.random() * 60 + 20,
    a: Math.random() * 0.04 + 0.01,
    color: Math.random() > 0.5 ? `rgba(255,80,0,` : `rgba(0,100,255,`,
    drift: (Math.random() - 0.5) * 0.02
  }));

  // ── STARS ─────────────────────────────────────────────────────
  const STARS = Array.from({ length: 600 }, () => ({
    x: Math.random() * 4000 - 2000,
    y: Math.random() * 4000 - 2000,
    s: Math.random() * 1.4 + 0.2,
    a: Math.random() * 0.7 + 0.1,
    f: (Math.random() - 0.5) * 0.006,
    c: Math.random() > 0.8 ? "255,180,100" : Math.random() > 0.5 ? "200,240,255" : "255,255,255"
  }));

  let frame = 0;

  function draw() {
    frame++;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;

    // ── NEBULA (background, very subtle) ────────────────────────
    NEBULA.forEach(n => {
      n.a += n.drift * 0.01;
      if (n.a > 0.06 || n.a < 0.005) n.drift *= -1;
      const grad = ctx.createRadialGradient(cx + n.x, cy + n.y, 0, cx + n.x, cy + n.y, n.r);
      grad.addColorStop(0, n.color + n.a + ")");
      grad.addColorStop(1, "transparent");
      ctx.beginPath();
      ctx.arc(cx + n.x, cy + n.y, n.r, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();
    });

    // ── STARS ────────────────────────────────────────────────────
    STARS.forEach(s => {
      s.a = Math.max(0.05, Math.min(0.9, s.a + s.f));
      if (s.a <= 0.05 || s.a >= 0.9) s.f *= -1;
      ctx.beginPath();
      ctx.arc((cx + s.x) % canvas.width, (cy + s.y) % canvas.height, s.s, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${s.c},${s.a * 0.6})`;
      ctx.fill();
    });

    // ── ORBIT RINGS (ellipses, subtle) ───────────────────────────
    PLANETS.forEach(p => {
      ctx.beginPath();
      ctx.ellipse(cx, cy, p.orbit, p.orbit * 0.32, 0, 0, Math.PI * 2);
      ctx.strokeStyle = "rgba(0,212,255,0.04)";
      ctx.lineWidth = 1;
      ctx.stroke();
    });

    // ── SUN (LYLA) ────────────────────────────────────────────────
    // Outer glow
    const sunGlow = ctx.createRadialGradient(cx, cy, 0, cx, cy, SUN.glow * 2);
    sunGlow.addColorStop(0, "rgba(0,212,255,0.2)");
    sunGlow.addColorStop(0.4, "rgba(0,212,255,0.06)");
    sunGlow.addColorStop(1, "transparent");
    ctx.beginPath();
    ctx.arc(cx, cy, SUN.glow * 2, 0, Math.PI * 2);
    ctx.fillStyle = sunGlow;
    ctx.fill();

    // Core
    const sunCore = ctx.createRadialGradient(cx, cy, 0, cx, cy, SUN.r);
    sunCore.addColorStop(0, "#ffffff");
    sunCore.addColorStop(0.4, "#00d4ff");
    sunCore.addColorStop(1, "#0044aa");
    ctx.beginPath();
    ctx.arc(cx, cy, SUN.r, 0, Math.PI * 2);
    ctx.fillStyle = sunCore;
    ctx.fill();

    // ── PLANETS ───────────────────────────────────────────────────
    PLANETS.forEach(p => {
      p.angle += p.speed;
      const x = cx + Math.cos(p.angle) * p.orbit;
      const y = cy + Math.sin(p.angle) * p.orbit * 0.32;

      // Faint connection line to center
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(x, y);
      ctx.strokeStyle = "rgba(0,212,255,0.025)";
      ctx.lineWidth = 1;
      ctx.stroke();

      // Planet glow
      const pg = ctx.createRadialGradient(x, y, 0, x, y, p.r * 4);
      pg.addColorStop(0, p.color + "55");
      pg.addColorStop(1, "transparent");
      ctx.beginPath();
      ctx.arc(x, y, p.r * 4, 0, Math.PI * 2);
      ctx.fillStyle = pg;
      ctx.fill();

      // Planet body
      ctx.beginPath();
      ctx.arc(x, y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.fill();

      // Label (only for labeled planets)
      if (p.label) {
        ctx.fillStyle = "rgba(200,240,255,0.5)";
        ctx.font = "8px 'Share Tech Mono', monospace";
        ctx.fillText(p.name, x + p.r + 4, y + 3);
      }

      // VEGA moons
      if (p.name === "VEGA") {
        VEGA_MOONS.forEach(m => {
          m.angle += m.speed;
          const mx = x + Math.cos(m.angle) * m.orbit;
          const my = y + Math.sin(m.angle) * m.orbit * 0.6;
          ctx.beginPath();
          ctx.arc(mx, my, m.r, 0, Math.PI * 2);
          ctx.fillStyle = m.color;
          ctx.fill();
        });
      }
    });

    // LYLA label
    ctx.fillStyle = "rgba(0,212,255,0.7)";
    ctx.font = "bold 9px 'Share Tech Mono', monospace";
    ctx.textAlign = "center";
    ctx.fillText("LYLA", cx, cy - SUN.r - 6);
    ctx.textAlign = "left";

    // ── SUPPLY CHAIN PULSE (every 180 frames) ────────────────────
    if (frame % 180 === 0) {
      // Ripple from center
      const ripple = { r: 0, max: 400, a: 0.15 };
      const drawRipple = () => {
        ripple.r += 3;
        ripple.a -= 0.003;
        if (ripple.r < ripple.max && ripple.a > 0) {
          ctx.beginPath();
          ctx.arc(cx, cy, ripple.r, 0, Math.PI * 2);
          ctx.strokeStyle = `rgba(0,212,255,${ripple.a})`;
          ctx.lineWidth = 1;
          ctx.stroke();
          requestAnimationFrame(drawRipple);
        }
      };
      drawRipple();
    }

    requestAnimationFrame(draw);
  }

  draw();
})();
