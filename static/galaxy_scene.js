/* galaxy_scene.js — King Diadem Decision Universe
   Decision nodes orbit the sun. Each planet = a LYLA kernel.
   Hover/click nodes to pulse the system.
*/
(function(){
  var canvas = document.getElementById('galaxy');
  if (!canvas) return;

  // Try WebGL first via Three.js, fall back to 2D canvas
  var ctx = canvas.getContext('2d', {alpha: false});
  var W, H, cx, cy, S;
  var t0 = performance.now();

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
    cx = W * 0.52; cy = H * 0.38;
    S = Math.min(W, H) * 0.46;
  }
  resize();
  window.addEventListener('resize', resize);

  // ── Stars ──
  var STAR_N = Math.min(5500, 3200 + Math.floor((window.innerWidth * window.innerHeight) / 3000));
  var stars = Array.from({length: STAR_N}, function() {
    var z = 0.08 + Math.random() * 0.92;
    var layer = z < 0.35 ? 0 : z < 0.7 ? 1 : 2;
    return {
      x: Math.random(), y: Math.random(), z: z, layer: layer,
      s: 0.4 + Math.pow(Math.random(), 1.2) * 2.8,
      tw: Math.random() * Math.PI * 2,
      sp: 0.008 + Math.random() * 0.038,
      warm: Math.random() > 0.42
    };
  });

  // ── Decision Orbit Nodes (LYLA Kernels) ──
  var NODES = [
    {label:'WATERLINE', key:'K5',  color:[45,212,191],  a:0.14, b:0.09, period:9000,  phase:0,    r:7,  desc:'ฐานขั้นต่ำ\nTreat · Trace · Stop', ring:false},
    {label:'STOP LINE', key:'K13', color:[255,80,80],   a:0.21, b:0.13, period:14000, phase:1.2,  r:6,  desc:'หยุดระบบทันที\nHarm detected → HALT', ring:false},
    {label:'STABILITY', key:'K11', color:[232,192,120], a:0.30, b:0.18, period:22000, phase:2.5,  r:8,  desc:'เสถียรก่อน optimize\nStabilize before improve', ring:true},
    {label:'AUDIT',     key:'K10', color:[160,130,255], a:0.39, b:0.24, period:32000, phase:0.8,  r:6,  desc:'หลักฐานก่อนเชื่อ\nEvidence, not narrative', ring:false},
    {label:'COMPASSION',key:'K2',  color:[255,145,60],  a:0.50, b:0.31, period:46000, phase:3.2,  r:7,  desc:'ลดอันตราย default\nWho suffers if we are wrong?', ring:false},
    {label:'ENTROPY',   key:'DHD', color:[160,195,255], a:0.63, b:0.39, period:65000, phase:1.9,  r:5,  desc:'0.1% drift รายวัน\nMeasure drift, not narrative', ring:false},
    {label:'RESTORE',   key:'K6',  color:[80,255,170],  a:0.78, b:0.48, period:90000, phase:4.3,  r:6,  desc:'ซ่อมก่อน normalize\nRepair harm first', ring:false},
  ];

  // ── Asteroid belt ──
  var BELT = Array.from({length: 380}, function() {
    return {g: 0.28+Math.random()*0.13, ph: Math.random()*Math.PI*2,
            sp: 0.000025+Math.random()*0.00006, sz: 0.5+Math.random()*2.5};
  });

  // ── Pulses (click/hover effect) ──
  var pulses = [];
  window.KD_pulse = function(label) {
    pulses.push({x: cx, y: cy, r: 0, maxR: Math.min(W,H)*0.55, alpha: 1});
    for (var i = 0; i < 5; i++) {
      (function(ii){ setTimeout(function(){
        pulses.push({x: cx, y: cy, r: 0, maxR: 60+ii*55, alpha: 0.7});
      }, ii*70); })(i);
    }
  };

  // ── Mouse ──
  var mx = -9999, my = -9999;
  canvas.addEventListener('mousemove', function(e){ mx=e.clientX; my=e.clientY; });
  canvas.addEventListener('click', function(e){
    var ts = performance.now() - t0;
    for (var i = 0; i < NODES.length; i++) {
      var pos = nodeXY(NODES[i], ts);
      if (Math.hypot(e.clientX-pos.x, e.clientY-pos.y) < NODES[i].r*3.5) {
        window.KD_pulse(NODES[i].label);
        break;
      }
    }
  });

  function nodeXY(n, ts) {
    var ang = (ts / n.period) * Math.PI * 2 + n.phase;
    return {x: cx + Math.cos(ang)*n.a*S, y: cy + Math.sin(ang)*n.b*S, ang: ang};
  }

  // ── Draw helpers ──
  function drawMilkyBand(ts) {
    ctx.save();
    ctx.translate(W*0.22, H*0.08);
    ctx.rotate(-0.42 + Math.sin(ts*0.00002)*0.012);
    var bw = Math.max(W,H)*1.85, bh = H*0.56;
    var g = ctx.createLinearGradient(0,-bh*0.5,0,bh*0.5);
    g.addColorStop(0,'rgba(255,240,220,0)');
    g.addColorStop(0.3,'rgba(140,90,200,0.18)');
    g.addColorStop(0.5,'rgba(30,200,185,0.22)');
    g.addColorStop(0.65,'rgba(255,170,90,0.17)');
    g.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=g; ctx.fillRect(-bw*0.2,-bh,bw,bh*2);
    ctx.globalCompositeOperation='lighter';
    var g2=ctx.createLinearGradient(bw*0.28,0,bw*0.72,0);
    g2.addColorStop(0,'rgba(255,200,120,0)');
    g2.addColorStop(0.5,'rgba(255,255,255,0.07)');
    g2.addColorStop(1,'rgba(100,220,255,0)');
    ctx.fillStyle=g2; ctx.fillRect(-bw*0.2,-bh,bw,bh*2);
    ctx.restore(); ctx.globalCompositeOperation='source-over';
  }

  function drawNebula() {
    var blobs=[
      {ox:.35,oy:.62,r:.52,c:'rgba(45,210,190,0.26)'},
      {ox:.72,oy:.28,r:.40,c:'rgba(255,100,40,0.24)'},
      {ox:.50,oy:.45,r:.88,c:'rgba(120,60,200,0.15)'},
      {ox:.12,oy:.35,r:.33,c:'rgba(255,175,80,0.20)'},
      {ox:.82,oy:.65,r:.30,c:'rgba(60,140,255,0.18)'},
      {ox:.08,oy:.80,r:.36,c:'rgba(200,80,255,0.16)'},
    ];
    ctx.globalCompositeOperation='screen';
    for (var i=0;i<blobs.length;i++){
      var b=blobs[i], nx=b.ox*W, ny=b.oy*H, rad=Math.max(W,H)*b.r;
      var gr=ctx.createRadialGradient(nx,ny,0,nx,ny,rad);
      gr.addColorStop(0,b.c); gr.addColorStop(1,'rgba(0,0,0,0)');
      ctx.fillStyle=gr; ctx.beginPath();
      ctx.ellipse(nx,ny,rad*0.82,rad*0.52,0.45,0,Math.PI*2); ctx.fill();
    }
    ctx.globalCompositeOperation='source-over';
  }

  function drawStars(ts) {
    for (var i=0;i<stars.length;i++){
      var s=stars[i];
      var par=s.layer===0?0.010:s.layer===1?0.022:0.038;
      var px=((s.x+ts*0.000014*par)%1+1)%1*W, py=s.y*H;
      var tw=0.5+0.5*Math.sin(ts*s.sp+s.tw);
      var sc=Math.max(0.4,s.s*s.z*tw);
      var a=Math.min(1,0.22+0.78*s.z*tw);
      var r=s.warm?255:208-Math.floor(30*s.z);
      var g=s.warm?228-Math.floor(40*s.z):234-Math.floor(20*s.z);
      var b=s.warm?188-Math.floor(80*s.z):255;
      ctx.beginPath(); ctx.arc(px,py,sc,0,Math.PI*2);
      ctx.fillStyle='rgba('+r+','+g+','+b+','+a+')'; ctx.fill();
      if(s.z>0.78&&tw>0.84){
        ctx.strokeStyle='rgba(255,252,240,'+(0.22*a)+')';
        ctx.lineWidth=0.4; ctx.beginPath();
        ctx.moveTo(px-sc*2.4,py); ctx.lineTo(px+sc*2.4,py);
        ctx.moveTo(px,py-sc*2.4); ctx.lineTo(px,py+sc*2.4);
        ctx.stroke();
      }
    }
  }

  function drawSun(ts) {
    var pulse=1+0.045*Math.sin(ts*0.00082);
    var R=Math.min(W,H)*0.145*pulse;
    // corona rays
    ctx.save(); ctx.translate(cx,cy);
    ctx.rotate((ts/70000)*Math.PI*2*0.4);
    ctx.globalCompositeOperation='lighter';
    for(var i=0;i<42;i++){
      var a=(i/42)*Math.PI*2;
      var w=R*(1.95+0.38*Math.sin(i*1.8));
      var x0=Math.cos(a)*R*0.2,y0=Math.sin(a)*R*0.2;
      var x1=Math.cos(a)*w,y1=Math.sin(a)*w;
      var grd=ctx.createLinearGradient(x0,y0,x1,y1);
      grd.addColorStop(0,'rgba(255,245,200,0.30)');
      grd.addColorStop(0.45,'rgba(255,120,40,0.07)');
      grd.addColorStop(1,'rgba(0,0,0,0)');
      ctx.strokeStyle=grd; ctx.lineWidth=2;
      ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x1,y1); ctx.stroke();
    }
    ctx.restore(); ctx.globalCompositeOperation='source-over';
    // halo
    ctx.globalCompositeOperation='lighter';
    var cor=ctx.createRadialGradient(cx,cy,R*0.06,cx,cy,R*2.1);
    cor.addColorStop(0,'rgba(255,255,250,0.94)');
    cor.addColorStop(0.07,'#ffe8a8');
    cor.addColorStop(0.20,'#ffb040');
    cor.addColorStop(0.42,'#ff5a18');
    cor.addColorStop(0.68,'#8b0a00');
    cor.addColorStop(1,'rgba(20,0,12,0)');
    ctx.beginPath(); ctx.arc(cx,cy,R*2.05,0,Math.PI*2);
    ctx.fillStyle=cor; ctx.fill();
    ctx.globalCompositeOperation='source-over';
    // core
    var core=ctx.createRadialGradient(cx,cy,0,cx,cy,R*0.56);
    core.addColorStop(0,'#fffef8');
    core.addColorStop(0.20,'#ffd060');
    core.addColorStop(0.52,'#ff7010');
    core.addColorStop(1,'#6a0a00');
    ctx.beginPath(); ctx.arc(cx,cy,R*0.52,0,Math.PI*2);
    ctx.fillStyle=core; ctx.fill();
    // LYLA text
    ctx.save();
    ctx.fillStyle='rgba(255,240,200,0.55)';
    ctx.font='bold '+Math.max(9,Math.floor(R*0.32))+'px "Share Tech Mono",monospace';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('LYLA', cx, cy);
    ctx.restore();
    // ring lines
    ctx.strokeStyle='rgba(255,230,190,0.18)'; ctx.lineWidth=1;
    for(var i=1;i<=3;i++){
      ctx.beginPath(); ctx.arc(cx,cy,R*(0.90+i*0.36),0,Math.PI*2); ctx.stroke();
    }
  }

  function drawOrbits() {
    ctx.strokeStyle='rgba(232,192,120,0.07)';
    ctx.lineWidth=0.8; ctx.setLineDash([4,10]);
    for(var i=0;i<NODES.length;i++){
      ctx.beginPath();
      ctx.ellipse(cx,cy,NODES[i].a*S,NODES[i].b*S,0,0,Math.PI*2);
      ctx.stroke();
    }
    ctx.setLineDash([]);
  }

  function drawBelt(ts) {
    ctx.fillStyle='rgba(220,215,255,0.28)';
    for(var i=0;i<BELT.length;i++){
      var b=BELT[i], ang=b.ph+ts*b.sp, rr=b.g*S;
      var xe=Math.cos(ang)*rr, ye=Math.sin(ang)*rr*0.58;
      ctx.fillRect(cx+xe-b.sz/2, cy+ye-b.sz/2, b.sz, b.sz);
    }
  }

  function drawNodes(ts) {
    var tip = document.getElementById('kd-tip');
    var hoveredAny = false;
    for(var i=0;i<NODES.length;i++){
      var n=NODES[i], pos=nodeXY(n,ts);
      var dist=Math.hypot(mx-pos.x,my-pos.y);
      var isHover=dist<n.r*3.8;
      if(isHover) hoveredAny=true;

      // trail
      for(var j=24;j>=0;j--){
        var prevTs=ts-j*(n.period/380);
        var pp=nodeXY(n,prevTs);
        var frac=j/24;
        var tr=n.color;
        ctx.beginPath(); ctx.arc(pp.x,pp.y,n.r*0.16*(1-frac),0,Math.PI*2);
        ctx.fillStyle='rgba('+tr[0]+','+tr[1]+','+tr[2]+','+(0.30*(1-frac))+')';
        ctx.fill();
      }

      // planet glow
      ctx.globalCompositeOperation='lighter';
      var glowR=n.r*(isHover?5.5:3.8);
      var glow=ctx.createRadialGradient(pos.x,pos.y,0,pos.x,pos.y,glowR);
      glow.addColorStop(0,'rgba('+n.color[0]+','+n.color[1]+','+n.color[2]+','+(isHover?0.55:0.32)+')');
      glow.addColorStop(1,'rgba(0,0,0,0)');
      ctx.beginPath(); ctx.arc(pos.x,pos.y,glowR,0,Math.PI*2);
      ctx.fillStyle=glow; ctx.fill();
      ctx.globalCompositeOperation='source-over';

      // planet body
      var dx=cx-pos.x,dy=cy-pos.y,dist2=Math.hypot(dx,dy)||1;
      var lx=dx/dist2,ly=dy/dist2;
      var pg=ctx.createRadialGradient(
        pos.x-lx*n.r*0.32,pos.y-ly*n.r*0.32,n.r*0.05,
        pos.x,pos.y,n.r
      );
      pg.addColorStop(0,'rgba(255,255,255,0.92)');
      pg.addColorStop(0.3,'rgba('+n.color[0]+','+n.color[1]+','+n.color[2]+',1)');
      pg.addColorStop(1,'rgba('+Math.floor(n.color[0]*0.18)+','+Math.floor(n.color[1]*0.18)+','+Math.floor(n.color[2]*0.18)+',1)');
      ctx.beginPath(); ctx.arc(pos.x,pos.y,n.r,0,Math.PI*2);
      ctx.fillStyle=pg; ctx.fill();

      // ring
      if(n.ring){
        ctx.save(); ctx.translate(pos.x,pos.y); ctx.rotate(pos.ang*0.5+0.5); ctx.scale(1,0.32);
        ctx.strokeStyle='rgba(245,220,180,0.55)'; ctx.lineWidth=1.5;
        ctx.beginPath(); ctx.arc(0,0,n.r*2.5,0,Math.PI*2); ctx.stroke();
        ctx.strokeStyle='rgba(180,155,110,0.30)'; ctx.lineWidth=2.5;
        ctx.beginPath(); ctx.arc(0,0,n.r*2.1,0,Math.PI*2); ctx.stroke();
        ctx.restore();
      }

      // connector line to sun
      ctx.save();
      ctx.strokeStyle='rgba('+n.color[0]+','+n.color[1]+','+n.color[2]+',0.06)';
      ctx.lineWidth=0.6; ctx.setLineDash([2,12]);
      ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(pos.x,pos.y); ctx.stroke();
      ctx.setLineDash([]); ctx.restore();

      // label
      ctx.save();
      ctx.fillStyle='rgba('+n.color[0]+','+n.color[1]+','+n.color[2]+','+(isHover?1:0.7)+')';
      ctx.font=(isHover?'bold ':'')+Math.max(7,n.r*0.85)+'px "Share Tech Mono",monospace';
      ctx.textAlign='center'; ctx.textBaseline='top';
      ctx.fillText(n.label, pos.x, pos.y+n.r+4);
      ctx.restore();

      // tooltip
      if(tip && isHover){
        tip.style.opacity='1';
        var tx=pos.x+18, ty=pos.y-18;
        if(tx+230>W) tx=pos.x-235;
        if(ty+80>H) ty=pos.y-90;
        tip.style.left=tx+'px'; tip.style.top=ty+'px';
        tip.innerHTML='<span style="color:rgba('+n.color[0]+','+n.color[1]+','+n.color[2]+',1);font-size:9px;">'+n.key+'</span><br>'+
          '<strong style="color:#e8f4ff;font-size:12px;">'+n.label+'</strong><br>'+
          '<span style="color:rgba(180,212,232,.65);font-size:10px;">'+n.desc.replace(/\n/g,'<br>')+'</span>';
      }
    }
    if(tip && !hoveredAny) tip.style.opacity='0';
  }

  function drawPulses() {
    pulses = pulses.filter(function(p){ return p.alpha>0.01; });
    for(var i=0;i<pulses.length;i++){
      var p=pulses[i];
      p.r += (p.maxR-p.r)*0.032;
      p.alpha *= 0.955;
      ctx.save();
      ctx.strokeStyle='rgba(232,192,120,'+p.alpha*0.5+')';
      ctx.lineWidth=1.5*p.alpha;
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.stroke();
      ctx.restore();
    }
  }

  // inject tooltip div
  if(!document.getElementById('kd-tip')){
    var tip=document.createElement('div'); tip.id='kd-tip';
    tip.style.cssText='position:fixed;pointer-events:none;z-index:9999;padding:10px 15px;'+
      'border-radius:10px;background:rgba(4,2,20,0.92);backdrop-filter:blur(14px);'+
      'border:1px solid rgba(232,192,120,0.25);color:#e8f4ff;max-width:225px;line-height:1.65;'+
      'font-family:"Share Tech Mono",monospace;font-size:11px;opacity:0;transition:opacity .18s;';
    document.body.appendChild(tip);
  }

  // birthday floaters
  var BDWORDS=['HAPPY','BIRTHDAY','KING DIADEM','LYLA','DRIFT·ZERO','FAIL·LESS','RESTORE'];
  var floaters=Array.from({length:9},function(_,i){
    return{
      word:BDWORDS[i%BDWORDS.length],
      x:Math.random(),y:Math.random()+0.2,
      speed:0.000025+Math.random()*0.00004,
      alpha:0.05+Math.random()*0.10,
      size:9+Math.random()*7,
      color:i%3===0?[232,192,120]:i%3===1?[45,212,191]:[160,130,255]
    };
  });

  function drawFloaters(ts){
    for(var i=0;i<floaters.length;i++){
      var f=floaters[i];
      f.y=((f.y-f.speed+1)%1);
      var px=f.x*W, py=f.y*H;
      ctx.save();
      ctx.fillStyle='rgba('+f.color[0]+','+f.color[1]+','+f.color[2]+','+f.alpha+')';
      ctx.font=f.size+'px "Share Tech Mono",monospace';
      ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.fillText(f.word,px,py);
      ctx.restore();
    }
  }

  // ── Main loop ──
  function frame(now){
    var ts = now - t0;
    ctx.fillStyle='#020110'; ctx.fillRect(0,0,W,H);
    drawMilkyBand(ts);
    drawNebula();
    drawStars(ts);
    drawFloaters(ts);
    drawBelt(ts);
    drawOrbits();
    drawPulses();
    // sun + planets in a save/restore so orbits aren't rotated
    drawNodes(ts);
    drawSun(ts);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
