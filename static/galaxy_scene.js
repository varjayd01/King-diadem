/* ============================================================
   KING DIADEM — galaxy_scene.js  v3.0
   Based on v2.1 — upgraded: centered system, deeper space,
   richer nebula, better sun, smoother planets, shooting stars
   ============================================================ */

(function () {
  if (typeof THREE !== 'undefined') return;

  const canvas = document.getElementById('galaxy');
  if (!canvas) return;
  const ctx = canvas.getContext('2d', { alpha: false });

  let W, H, cx, cy, S;

  function resize() {
    W  = canvas.width  = window.innerWidth;
    H  = canvas.height = window.innerHeight;
    /* กึ่งกลางจอเสมอ — แทน 0.52 / 0.38 */
    cx = W * 0.50;
    cy = H * 0.50;
    S  = Math.min(W, H) * 0.44;
  }
  resize();
  window.addEventListener('resize', resize);

  /* ── Stars ── */
  const STAR_N = Math.min(7000, 4200 + Math.floor((window.innerWidth * window.innerHeight) / 2400));
  const stars = Array.from({ length: STAR_N }, () => {
    const z     = 0.1 + Math.random() * 0.9;
    const layer = z < 0.35 ? 0 : z < 0.7 ? 1 : 2;
    return {
      x:       Math.random(),
      y:       Math.random(),
      z,
      layer,
      s:       0.45 + Math.pow(Math.random(), 1.1) * 2.9,
      tw:      Math.random() * Math.PI * 2,
      sp:      0.008 + Math.random() * 0.038,
      warm:    Math.random() > 0.40,
      vx:      (Math.random() - 0.5) * 0.000045,
      special: Math.random() < 0.04 ? (Math.random() < 0.5 ? 'blue' : 'orange') : null
    };
  });

  /* ── Kepler orbits ── */
  const ORBIT_REF_MS = 62000;
  const refIdx = 2;
  const planets = [
    { a: 0.16, b: 0.140, orn: 0.08,  r: 3.8, rgb: [200,210,255], ring: 0, phase: Math.random()*6.283 },
    { a: 0.24, b: 0.200, orn: 0.03,  r: 4.5, rgb: [255,125,90],  ring: 0, phase: Math.random()*6.283 },
    { a: 0.32, b: 0.275, orn: 0.11,  r: 6.5, rgb: [205,170,115], ring: 1, phase: Math.random()*6.283 },
    { a: 0.42, b: 0.345, orn: 0.05,  r: 5.2, rgb: [65,130,255],  ring: 0, phase: Math.random()*6.283 },
    { a: 0.54, b: 0.405, orn: 0.025, r: 4.0, rgb: [195,105,195], ring: 0, phase: Math.random()*6.283 },
    { a: 0.67, b: 0.490, orn: 0.13,  r: 3.2, rgb: [145,210,255], ring: 0, phase: Math.random()*6.283 },
    { a: 0.82, b: 0.560, orn: 0.065, r: 2.8, rgb: [172,182,212], ring: 0, phase: Math.random()*6.283 }
  ];
  const refMean = (planets[refIdx].a + planets[refIdx].b) * 0.5;
  for (const p of planets) {
    const mean = (p.a + p.b) * 0.5;
    p.periodMs = ORBIT_REF_MS * Math.pow(Math.max(0.08, mean) / Math.max(0.08, refMean), 1.5);
  }

  /* ── Asteroid belt ── */
  const belt = Array.from({ length: 520 }, () => ({
    g:  0.475 + Math.random() * 0.13,
    ph: Math.random() * 6.283,
    sp: 0.000035 + Math.random() * 0.000065,
    a:  0.3 + Math.random() * 0.9
  }));

  /* ── Shooting stars ── */
  const shooters = [];
  function spawnShooter() {
    if (shooters.length >= 3) return;
    shooters.push({
      x:    Math.random() * W,
      y:    Math.random() * H * 0.5,
      vx:   3 + Math.random() * 5,
      vy:   1.5 + Math.random() * 3,
      len:  60 + Math.random() * 100,
      life: 1.0,
      decay:0.016 + Math.random() * 0.018
    });
  }
  setInterval(spawnShooter, 3800 + Math.random() * 4000);

  /* ── Milky Way band ── */
  function drawMilkyBand(tt) {
    ctx.save();
    ctx.translate(W * 0.14, H * 0.04);
    ctx.rotate(-0.38 + Math.sin(tt * 0.000018) * 0.010);
    const bw = Math.max(W, H) * 2.1;
    const bh = H * 0.64;
    const g  = ctx.createLinearGradient(0, -bh * 0.5, 0, bh * 0.5);
    g.addColorStop(0,    'rgba(255,240,220,0)');
    g.addColorStop(0.28, 'rgba(120,70,190,0.14)');
    g.addColorStop(0.50, 'rgba(28,195,178,0.18)');
    g.addColorStop(0.66, 'rgba(255,165,80,0.14)');
    g.addColorStop(0.84, 'rgba(255,215,170,0.06)');
    g.addColorStop(1,    'rgba(0,0,0,0)');
    ctx.fillStyle = g;
    ctx.fillRect(-bw * 0.18, -bh, bw, bh * 2);
    ctx.globalCompositeOperation = 'lighter';
    const g2 = ctx.createLinearGradient(bw * 0.26, 0, bw * 0.74, 0);
    g2.addColorStop(0,   'rgba(255,200,120,0)');
    g2.addColorStop(0.5, 'rgba(255,255,255,0.055)');
    g2.addColorStop(1,   'rgba(100,220,255,0)');
    ctx.fillStyle = g2;
    ctx.fillRect(-bw * 0.18, -bh, bw, bh * 2);
    ctx.restore();
    ctx.globalCompositeOperation = 'source-over';
  }

  /* ── Nebula colour clouds ── */
  function drawNebulaClouds() {
    const blobs = [
      { ox:0.08, oy:0.18, rx:0.38, ry:0.32, rot:0.30,  c1:'rgba(30,160,220,0.16)',  c2:'rgba(10,30,80,0)'  },
      { ox:0.88, oy:0.22, rx:0.32, ry:0.28, rot:-0.20, c1:'rgba(255,110,50,0.15)',  c2:'rgba(60,10,30,0)'  },
      { ox:0.50, oy:0.50, rx:0.75, ry:0.60, rot:0.10,  c1:'rgba(120,60,185,0.09)',  c2:'rgba(0,0,0,0)'     },
      { ox:0.18, oy:0.78, rx:0.30, ry:0.24, rot:0.50,  c1:'rgba(255,190,120,0.13)', c2:'rgba(0,0,0,0)'     },
      { ox:0.80, oy:0.72, rx:0.28, ry:0.22, rot:-0.40, c1:'rgba(60,150,255,0.11)',  c2:'rgba(0,0,0,0)'     },
      { ox:0.35, oy:0.92, rx:0.45, ry:0.20, rot:0.15,  c1:'rgba(45,215,195,0.10)',  c2:'rgba(0,0,0,0)'     }
    ];
    ctx.globalCompositeOperation = 'screen';
    for (const b of blobs) {
      const nx  = b.ox * W, ny = b.oy * H;
      const rrx = Math.max(W, H) * b.rx;
      const rry = Math.max(W, H) * b.ry;
      const gr  = ctx.createRadialGradient(nx, ny, 0, nx, ny, rrx);
      gr.addColorStop(0, b.c1);
      gr.addColorStop(1, b.c2);
      ctx.save();
      ctx.translate(nx, ny);
      ctx.rotate(b.rot);
      ctx.scale(1, rry / rrx);
      ctx.translate(-nx, -ny);
      ctx.fillStyle = gr;
      ctx.beginPath();
      ctx.arc(nx, ny, rrx, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
    ctx.globalCompositeOperation = 'source-over';
  }

  /* ── Stars draw ── */
  function drawStars(tt) {
    const drift = tt * 0.000016;
    for (const s of stars) {
      const par = s.layer === 0 ? 0.010 : s.layer === 1 ? 0.024 : 0.042;
      const px  = ((s.x + drift * par + s.vx * tt) % 1 + 1) % 1 * W;
      const py  = s.y * H;
      const tw  = 0.5 + 0.5 * Math.sin(tt * s.sp + s.tw);
      const sc  = Math.max(0.38, s.s * s.z * tw * (0.85 + s.layer * 0.12));
      const a   = Math.min(1, 0.20 + 0.75 * s.z * tw);
      let r, g, b;
      if      (s.special === 'blue')   { r=160; g=200; b=255; }
      else if (s.special === 'orange') { r=255; g=160; b=80;  }
      else if (s.warm) { r=255; g=230-Math.floor(38*s.z); b=185-Math.floor(78*s.z); }
      else             { r=205-Math.floor(28*s.z); g=232-Math.floor(18*s.z); b=255;  }
      ctx.beginPath();
      ctx.arc(px, py, sc, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba('+r+','+g+','+b+','+a+')';
      ctx.fill();
      if (s.z > 0.78 && tw > 0.80) {
        const arm = sc * 2.4;
        ctx.strokeStyle = 'rgba(255,250,230,'+(0.16*a)+')';
        ctx.lineWidth = 0.5;
        ctx.beginPath();
        ctx.moveTo(px-arm,py); ctx.lineTo(px+arm,py);
        ctx.moveTo(px,py-arm); ctx.lineTo(px,py+arm);
        ctx.stroke();
      }
    }
  }

  /* ── Shooting stars ── */
  function drawShooters() {
    for (let i = shooters.length - 1; i >= 0; i--) {
      const s = shooters[i];
      s.x += s.vx; s.y += s.vy; s.life -= s.decay;
      if (s.life <= 0) { shooters.splice(i, 1); continue; }
      const tail = ctx.createLinearGradient(
        s.x - s.vx * s.len * 0.1, s.y - s.vy * s.len * 0.1, s.x, s.y
      );
      tail.addColorStop(0, 'rgba(255,255,255,0)');
      tail.addColorStop(1, 'rgba(255,255,220,'+(s.life*0.9)+')');
      ctx.strokeStyle = tail;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(s.x - s.vx*s.len*0.1, s.y - s.vy*s.len*0.1);
      ctx.lineTo(s.x, s.y);
      ctx.stroke();
    }
  }

  /* ── Sun ── */
  function drawSunCorona(tt) {
    const pulse = 1 + 0.048 * Math.sin(tt * 0.00082);
    const R     = Math.min(W, H) * 0.135 * pulse;
    const spin  = (tt / ORBIT_REF_MS) * Math.PI * 2;

    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(spin * 0.32);
    ctx.globalCompositeOperation = 'lighter';
    const rays = 48;
    for (let i = 0; i < rays; i++) {
      const a   = (i / rays) * Math.PI * 2;
      const w   = R * (1.85 + 0.50 * Math.sin(i * 1.618 + tt * 0.00025));
      const x0  = Math.cos(a) * R * 0.20, y0 = Math.sin(a) * R * 0.20;
      const x1  = Math.cos(a) * w,        y1 = Math.sin(a) * w;
      const grd = ctx.createLinearGradient(x0, y0, x1, y1);
      grd.addColorStop(0,    'rgba(255,240,200,0.24)');
      grd.addColorStop(0.35, 'rgba(255,130,50,0.10)');
      grd.addColorStop(1,    'rgba(0,0,0,0)');
      ctx.strokeStyle = grd;
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      ctx.moveTo(x0, y0); ctx.lineTo(x1, y1);
      ctx.stroke();
    }
    ctx.restore();
    ctx.globalCompositeOperation = 'source-over';

    /* outer halo */
    const cor = ctx.createRadialGradient(cx, cy, R*0.05, cx, cy, R*2.4);
    cor.addColorStop(0,    'rgba(255,255,248,0.96)');
    cor.addColorStop(0.06, '#ffeaaa');
    cor.addColorStop(0.18, '#ffb845');
    cor.addColorStop(0.38, '#ff5c1a');
    cor.addColorStop(0.62, '#aa1000');
    cor.addColorStop(1,    'rgba(20,0,15,0)');
    ctx.globalCompositeOperation = 'lighter';
    ctx.beginPath();
    ctx.arc(cx, cy, R * 2.2, 0, Math.PI * 2);
    ctx.fillStyle = cor;
    ctx.fill();
    ctx.globalCompositeOperation = 'source-over';

    /* core */
    const core = ctx.createRadialGradient(cx-R*0.14, cy-R*0.14, 0, cx, cy, R*0.60);
    core.addColorStop(0,    '#fffef8');
    core.addColorStop(0.18, '#ffe060');
    core.addColorStop(0.48, '#ff7818');
    core.addColorStop(1,    '#780c00');
    ctx.beginPath();
    ctx.arc(cx, cy, R * 0.57, 0, Math.PI * 2);
    ctx.fillStyle = core;
    ctx.fill();

    /* orbit hint rings */
    ctx.strokeStyle = 'rgba(255,230,190,0.18)';
    ctx.lineWidth   = 0.9;
    for (let i = 1; i <= 4; i++) {
      ctx.beginPath();
      ctx.arc(cx, cy, R * (0.90 + i * 0.30), 0, Math.PI * 2);
      ctx.stroke();
    }
  }

  /* ── Planet helpers ── */
  function planetXY(p, tt) {
    const ang = (tt / p.periodMs) * (Math.PI * 2) + p.phase;
    const xe  = Math.cos(ang) * p.a * S;
    const ye  = Math.sin(ang) * p.b * S;
    const co  = Math.cos(p.orn), si = Math.sin(p.orn);
    return { x: cx + xe*co - ye*si, y: cy + xe*si + ye*co, ang };
  }

  function drawOrbits() {
    ctx.lineWidth = 0.8;
    for (const p of planets) {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(p.orn);
      ctx.strokeStyle = 'rgba(255,245,225,0.10)';
      ctx.setLineDash([4, 8]);
      ctx.beginPath();
      ctx.ellipse(0, 0, p.a*S, p.b*S, 0, 0, Math.PI*2);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.restore();
    }
  }

  function drawAsteroidBelt(tt) {
    ctx.fillStyle = 'rgba(220,215,245,0.30)';
    for (const ro of belt) {
      const ang = ro.ph + tt * ro.sp;
      const rr  = ro.g * S;
      const xe  = Math.cos(ang) * rr;
      const ye  = Math.sin(ang) * rr * 0.88;
      const co  = Math.cos(0.09), si = Math.sin(0.09);
      const x   = cx + xe*co - ye*si;
      const y   = cy + xe*si + ye*co;
      ctx.fillRect(x, y, ro.a, ro.a);
    }
  }

  function drawPlanetBody(x, y, r, rgb, p, ang) {
    const dx = cx-x, dy = cy-y;
    const dist = Math.hypot(dx,dy)||1;
    const lx = dx/dist, ly = dy/dist;
    const gx = x - lx*r*0.88, gy = y - ly*r*0.88;

    const lit = ctx.createRadialGradient(gx, gy, r*0.08, x, y, r*1.12);
    lit.addColorStop(0,    'rgba(255,255,255,0.88)');
    lit.addColorStop(0.32, 'rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+',1)');
    lit.addColorStop(1,    'rgba('+Math.floor(rgb[0]*0.22)+','+Math.floor(rgb[1]*0.20)+','+Math.floor(rgb[2]*0.25)+',1)');
    ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2);
    ctx.fillStyle = lit; ctx.fill();

    ctx.save();
    ctx.translate(x,y);
    ctx.rotate(ang*0.38 + p.phase);
    ctx.globalCompositeOperation = 'multiply';
    ctx.fillStyle = 'rgba(0,4,16,0.38)';
    ctx.beginPath();
    ctx.ellipse(-r*0.32, 0, r*1.04, r*0.90, 0, 0, Math.PI*2);
    ctx.fill();
    ctx.restore();
    ctx.globalCompositeOperation = 'source-over';

    /* atmosphere */
    const atm = ctx.createRadialGradient(x,y,r*0.85,x,y,r*1.55);
    atm.addColorStop(0,'rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+',0.22)');
    atm.addColorStop(1,'rgba(0,0,0,0)');
    ctx.beginPath(); ctx.arc(x,y,r*1.55,0,Math.PI*2);
    ctx.fillStyle=atm; ctx.fill();

    /* glow */
    const glow = ctx.createRadialGradient(x,y,0,x,y,r*4.8);
    glow.addColorStop(0,'rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+',0.32)');
    glow.addColorStop(1,'rgba(0,0,0,0)');
    ctx.beginPath(); ctx.arc(x,y,r*4.8,0,Math.PI*2);
    ctx.fillStyle=glow; ctx.fill();
  }

  function drawRings(x, y, r, ang) {
    ctx.save();
    ctx.translate(x,y);
    ctx.rotate(ang*0.60+0.5);
    ctx.scale(1,0.34);
    ctx.strokeStyle='rgba(242,222,185,0.44)'; ctx.lineWidth=2.2;
    ctx.beginPath(); ctx.arc(0,0,r*2.58,0,Math.PI*2); ctx.stroke();
    ctx.strokeStyle='rgba(200,175,125,0.30)'; ctx.lineWidth=3.5;
    ctx.beginPath(); ctx.arc(0,0,r*2.16,0,Math.PI*2); ctx.stroke();
    ctx.strokeStyle='rgba(160,140,100,0.16)'; ctx.lineWidth=1.5;
    ctx.beginPath(); ctx.arc(0,0,r*1.78,0,Math.PI*2); ctx.stroke();
    ctx.restore();
  }

  function drawPlanets(tt) {
    const order = planets.map((p,i)=>({i,p,y:planetXY(p,tt).y})).sort((a,b)=>a.y-b.y);
    for (const {p} of order) {
      const {x,y,ang} = planetXY(p,tt);
      if (p.ring) drawRings(x,y,p.r,ang);
      drawPlanetBody(x,y,p.r,p.rgb,p,ang);
    }
  }

  /* ── Main loop ── */
  function frame(t) {
    ctx.fillStyle = '#01010b';
    ctx.fillRect(0, 0, W, H);

    drawMilkyBand(t);
    drawNebulaClouds();
    drawStars(t);
    drawShooters();

    /* หมุนระบบสุริยะรอบ center ช้ามาก */
    const deck = (t / ORBIT_REF_MS) * 0.08;
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
