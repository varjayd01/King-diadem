/* ============================================================
   KING DIADEM — galaxy_scene.js  v2.1
   จักรวาลสวยขึ้น: ดาวสว่าง, nebula มีสี, overlay บางลง
   ============================================================ */

(function () {
  /* ถ้า Three.js โหลดแล้ว ปล่อยให้ galaxy_scene.js หลักทำงาน */
  if (typeof THREE !== 'undefined') return;

  const canvas = document.getElementById('galaxy');
  if (!canvas) return;
  const ctx = canvas.getContext('2d', { alpha: false });

  let W, H, cx, cy, S;

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
    cx = W * 0.52;
    cy = H * 0.38;
    S  = Math.min(W, H) * 0.46;
  }
  resize();
  window.addEventListener('resize', resize);

  /* ── Stars ── */
  const STAR_N = Math.min(6000, 3800 + Math.floor((W * H) / 2800));
  const stars = Array.from({ length: STAR_N }, () => {
    const z     = 0.1 + Math.random() * 0.9;
    const layer = z < 0.35 ? 0 : (z < 0.7 ? 1 : 2);
    return {
      x:    Math.random(),
      y:    Math.random(),
      z,
      layer,
      s:    0.4 + Math.pow(Math.random(), 1.2) * 2.8,   // bigger stars
      tw:   Math.random() * Math.PI * 2,
      sp:   0.01 + Math.random() * 0.04,
      warm: Math.random() > 0.42,
      vx:   (Math.random() - 0.5) * 0.00005
    };
  });

  /* ── Kepler orbits ── */
  const ORBIT_REF_MS = 60000;
  const refIdx = 2;
  const planets = [
    { a: 0.19, b: 0.165, orn: 0.11, r: 4.2, rgb: [200, 210, 255], ring: 0, phase: Math.random() * 6.283 },
    { a: 0.27, b: 0.225, orn: 0.04, r: 4.8, rgb: [255, 120, 85],  ring: 0, phase: Math.random() * 6.283 },
    { a: 0.34, b: 0.30,  orn: 0.12, r: 6.8, rgb: [210, 175, 120], ring: 1, phase: Math.random() * 6.283 },
    { a: 0.44, b: 0.36,  orn: 0.06, r: 5.6, rgb: [70,  130, 255], ring: 0, phase: Math.random() * 6.283 },
    { a: 0.56, b: 0.42,  orn: 0.03, r: 4.1, rgb: [200, 110, 200], ring: 0, phase: Math.random() * 6.283 },
    { a: 0.70, b: 0.50,  orn: 0.14, r: 3.4, rgb: [150, 210, 255], ring: 0, phase: Math.random() * 6.283 },
    { a: 0.86, b: 0.58,  orn: 0.07, r: 2.9, rgb: [175, 185, 215], ring: 0, phase: Math.random() * 6.283 }
  ];
  const refMean = (planets[refIdx].a + planets[refIdx].b) * 0.5;
  for (const p of planets) {
    const mean = (p.a + p.b) * 0.5;
    p.periodMs = ORBIT_REF_MS * Math.pow(Math.max(0.08, mean) / Math.max(0.08, refMean), 1.5);
  }

  /* ── Asteroid belt ── */
  const beltN = 480;
  const belt  = Array.from({ length: beltN }, () => ({
    g:  0.48 + Math.random() * 0.14,
    ph: Math.random() * 6.283,
    sp: 0.00004 + Math.random() * 0.00007,
    a:  0.025 + Math.random() * 0.06
  }));

  /* ── Milky way band ── */
  function drawMilkyBand(tt) {
    ctx.save();
    ctx.translate(W * 0.18, H * 0.06);
    ctx.rotate(-0.40 + Math.sin(tt * 0.00002) * 0.012);
    const bw = Math.max(W, H) * 1.9;
    const bh = H * 0.60;
    const g  = ctx.createLinearGradient(0, -bh * 0.5, 0, bh * 0.5);
    g.addColorStop(0,    'rgba(255,240,220,0)');
    g.addColorStop(0.30, 'rgba(140,90,200,0.12)');
    g.addColorStop(0.50, 'rgba(30,200,185,0.16)');
    g.addColorStop(0.65, 'rgba(255,170,90,0.13)');
    g.addColorStop(0.82, 'rgba(255,220,180,0.06)');
    g.addColorStop(1,    'rgba(0,0,0,0)');
    ctx.fillStyle = g;
    ctx.fillRect(-bw * 0.2, -bh, bw, bh * 2);

    ctx.globalCompositeOperation = 'lighter';
    const g2 = ctx.createLinearGradient(bw * 0.28, 0, bw * 0.72, 0);
    g2.addColorStop(0,   'rgba(255,200,120,0)');
    g2.addColorStop(0.5, 'rgba(255,255,255,0.05)');
    g2.addColorStop(1,   'rgba(100,220,255,0)');
    ctx.fillStyle = g2;
    ctx.fillRect(-bw * 0.2, -bh, bw, bh * 2);
    ctx.restore();
    ctx.globalCompositeOperation = 'source-over';
  }

  /* ── Nebula colour clouds ── */
  function drawNebulaClouds() {
    const blobs = [
      { ox: 0.30, oy: 0.65, r: 0.55, c1: 'rgba(45,210,190,0.18)',  c2: 'rgba(20,40,80,0)'  },
      { ox: 0.74, oy: 0.25, r: 0.42, c1: 'rgba(255,130,60,0.16)',  c2: 'rgba(80,20,40,0)'  },
      { ox: 0.50, oy: 0.44, r: 0.90, c1: 'rgba(140,80,200,0.10)',  c2: 'rgba(0,0,0,0)'     },
      { ox: 0.10, oy: 0.32, r: 0.34, c1: 'rgba(255,200,140,0.12)', c2: 'rgba(0,0,0,0)'     },
      { ox: 0.85, oy: 0.70, r: 0.30, c1: 'rgba(80,160,255,0.10)',  c2: 'rgba(0,0,0,0)'     }
    ];
    ctx.globalCompositeOperation = 'screen';
    for (const b of blobs) {
      const nx = b.ox * W, ny = b.oy * H, rad = Math.max(W, H) * b.r;
      const gr = ctx.createRadialGradient(nx, ny, 0, nx, ny, rad);
      gr.addColorStop(0, b.c1);
      gr.addColorStop(1, b.c2);
      ctx.fillStyle = gr;
      ctx.beginPath();
      ctx.ellipse(nx, ny, rad * 0.88, rad * 0.56, 0.45, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalCompositeOperation = 'source-over';
  }

  /* ── Stars draw ── */
  function drawStars(tt) {
    const drift = tt * 0.000018;
    for (const s of stars) {
      const par = s.layer === 0 ? 0.012 : s.layer === 1 ? 0.026 : 0.044;
      const px  = ((s.x + drift * par + s.vx * tt) % 1 + 1) % 1 * W;
      const py  = s.y * H;
      const tw  = 0.5 + 0.5 * Math.sin(tt * s.sp + s.tw);
      const sc  = Math.max(0.4, s.s * s.z * tw * (0.88 + s.layer * 0.10));
      /* brighter alpha */
      const a   = Math.min(1, 0.18 + 0.72 * s.z * tw);
      let r, g, b;
      if (s.warm) { r = 255; g = 228 - Math.floor(40 * s.z); b = 188 - Math.floor(80 * s.z); }
      else         { r = 208 - Math.floor(30 * s.z); g = 234 - Math.floor(20 * s.z); b = 255; }
      ctx.beginPath();
      ctx.arc(px, py, sc, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
      ctx.fill();
      /* cross-hairs for bright stars */
      if (s.z > 0.75 && tw > 0.82) {
        ctx.strokeStyle = 'rgba(255,250,235,' + (0.18 * a) + ')';
        ctx.lineWidth = 0.5;
        ctx.beginPath();
        ctx.moveTo(px - sc * 2.2, py); ctx.lineTo(px + sc * 2.2, py);
        ctx.moveTo(px, py - sc * 2.2); ctx.lineTo(px, py + sc * 2.2);
        ctx.stroke();
      }
    }
  }

  /* ── Sun corona ── */
  function drawSunCorona(tt) {
    const pulse = 1 + 0.045 * Math.sin(tt * 0.00085);
    const R     = Math.min(W, H) * 0.142 * pulse;
    const spin  = (tt / ORBIT_REF_MS) * Math.PI * 2;

    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(spin * 0.35);
    ctx.globalCompositeOperation = 'lighter';
    const rays = 44;
    for (let i = 0; i < rays; i++) {
      const a  = (i / rays) * Math.PI * 2;
      const w  = R * (1.90 + 0.42 * Math.sin(i * 1.7));
      const x0 = Math.cos(a) * R * 0.22, y0 = Math.sin(a) * R * 0.22;
      const x1 = Math.cos(a) * w,        y1 = Math.sin(a) * w;
      const grd = ctx.createLinearGradient(x0, y0, x1, y1);
      grd.addColorStop(0, 'rgba(255,240,220,0.22)');
      grd.addColorStop(0.4, 'rgba(255,120,40,0.08)');
      grd.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.strokeStyle = grd;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(x0, y0); ctx.lineTo(x1, y1);
      ctx.stroke();
    }
    ctx.restore();
    ctx.globalCompositeOperation = 'source-over';

    /* halo */
    const cor = ctx.createRadialGradient(cx, cy, R * 0.06, cx, cy, R * 2.2);
    cor.addColorStop(0,    'rgba(255,255,250,0.95)');
    cor.addColorStop(0.07, '#ffe8a8');
    cor.addColorStop(0.20, '#ffb040');
    cor.addColorStop(0.42, '#ff5a18');
    cor.addColorStop(0.68, '#b01000');
    cor.addColorStop(1,    'rgba(25,0,18,0)');
    ctx.globalCompositeOperation = 'lighter';
    ctx.beginPath();
    ctx.arc(cx, cy, R * 2.05, 0, Math.PI * 2);
    ctx.fillStyle = cor;
    ctx.fill();
    ctx.globalCompositeOperation = 'source-over';

    /* core */
    const core = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * 0.62);
    core.addColorStop(0,    '#fffef8');
    core.addColorStop(0.22, '#ffd060');
    core.addColorStop(0.52, '#ff7010');
    core.addColorStop(1,    '#7a0d00');
    ctx.beginPath();
    ctx.arc(cx, cy, R * 0.58, 0, Math.PI * 2);
    ctx.fillStyle = core;
    ctx.fill();

    /* orbit rings hint */
    ctx.strokeStyle = 'rgba(255,230,190,0.22)';
    ctx.lineWidth = 1.0;
    for (let i = 1; i <= 4; i++) {
      ctx.beginPath();
      ctx.arc(cx, cy, R * (0.92 + i * 0.32), 0, Math.PI * 2);
      ctx.stroke();
    }
  }

  /* ── Helpers ── */
  function planetXY(p, tt) {
    const ang = (tt / p.periodMs) * (Math.PI * 2) + p.phase;
    const xe  = Math.cos(ang) * p.a * S;
    const ye  = Math.sin(ang) * p.b * S;
    const co  = Math.cos(p.orn), si = Math.sin(p.orn);
    return { x: cx + xe * co - ye * si, y: cy + xe * si + ye * co, ang };
  }

  function drawOrbits() {
    ctx.lineWidth = 0.85;
    for (const p of planets) {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(p.orn);
      ctx.strokeStyle = 'rgba(255,245,230,0.13)';
      ctx.beginPath();
      ctx.ellipse(0, 0, p.a * S, p.b * S, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }
  }

  function drawAsteroidBelt(tt) {
    ctx.fillStyle = 'rgba(230,220,255,0.38)';
    for (const ro of belt) {
      const ang = ro.ph + tt * ro.sp;
      const rr  = ro.g * S;
      const xe  = Math.cos(ang) * rr;
      const ye  = Math.sin(ang) * rr * 0.88;
      const co  = Math.cos(0.09), si = Math.sin(0.09);
      const x   = cx + xe * co - ye * si;
      const y   = cy + xe * si + ye * co;
      ctx.fillRect(x, y, ro.a, ro.a);
    }
  }

  function drawPlanetBody(x, y, r, rgb, tt, p, ang) {
    const dx = cx - x, dy = cy - y;
    const dist = Math.hypot(dx, dy) || 1;
    const lx = dx / dist, ly = dy / dist;
    const gx = x - lx * r * 0.85, gy = y - ly * r * 0.85;
    const lit = ctx.createRadialGradient(gx, gy, r * 0.1, x, y, r * 1.15);
    lit.addColorStop(0,    'rgba(255,255,255,0.92)');
    lit.addColorStop(0.35, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',1)');
    lit.addColorStop(1,    'rgba(' + Math.floor(rgb[0]*0.25) + ',' + Math.floor(rgb[1]*0.22) + ',' + Math.floor(rgb[2]*0.28) + ',1)');
    ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = lit; ctx.fill();

    /* shadow */
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(ang * 0.4 + p.phase);
    ctx.globalCompositeOperation = 'multiply';
    ctx.fillStyle = 'rgba(0,5,18,0.40)';
    ctx.beginPath();
    ctx.ellipse(-r * 0.35, 0, r * 1.05, r * 0.92, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
    ctx.globalCompositeOperation = 'source-over';

    /* glow */
    const glow = ctx.createRadialGradient(x, y, 0, x, y, r * 5);
    glow.addColorStop(0, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0.38)');
    glow.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.beginPath(); ctx.arc(x, y, r * 5, 0, Math.PI * 2);
    ctx.fillStyle = glow; ctx.fill();
  }

  function drawRings(x, y, r, ang) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang * 0.62 + 0.5); ctx.scale(1, 0.36);
    ctx.strokeStyle = 'rgba(245,225,190,0.48)'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.arc(0, 0, r * 2.55, 0, Math.PI * 2); ctx.stroke();
    ctx.strokeStyle = 'rgba(180,160,120,0.28)'; ctx.lineWidth = 2.8;
    ctx.beginPath(); ctx.arc(0, 0, r * 2.2,  0, Math.PI * 2); ctx.stroke();
    ctx.restore();
  }

  function drawPlanets(tt) {
    const order = planets.map((p, i) => ({ i, p, y: planetXY(p, tt).y })).sort((a, b) => a.y - b.y);
    for (const { i, p } of order) {
      const { x, y, ang } = planetXY(p, tt);
      if (p.ring) drawRings(x, y, p.r, ang);
      drawPlanetBody(x, y, p.r, p.rgb, tt, p, ang);
    }
  }

  /* ── Render loop ── */
  function frame(t) {
    /* Deep space base — slightly lighter than pure black so stars pop */
    ctx.fillStyle = '#01010c';
    ctx.fillRect(0, 0, W, H);

    drawMilkyBand(t);
    drawNebulaClouds();
    drawStars(t);

    /* Rotate solar system plane slowly */
    const deck = (t / ORBIT_REF_MS) * (Math.PI * 2);
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(deck);
    ctx.translate(-cx, -cy);

    drawSunCorona(t);
    drawOrbits();
    drawAsteroidBelt(t);
    drawPlanets(t);

    ctx.restore();
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
