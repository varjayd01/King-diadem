// static/galaxy_scene.js — LYLA sun + 7 decision nodes (Three.js r128)
(function () {
  var canvas = document.getElementById("galaxy");
  if (!canvas || typeof THREE === "undefined") return;

  var renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    alpha: false,
    powerPreference: "high-performance",
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  var scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000008);
  scene.fog = new THREE.FogExp2(0x020306, 0.00014);

  var camera = new THREE.PerspectiveCamera(48, 1, 10, 120000);
  /* มุมสูง: มองระนาบโคจรแบบ bird's-eye ลาดเล็กน้อย */
  camera.position.set(0, 5600, 5200);

  function resize() {
    var w = window.innerWidth;
    var h = window.innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  resize();
  window.addEventListener("resize", resize);

  function makeNebulaTexture() {
    var c = document.createElement("canvas");
    c.width = 1024;
    c.height = 1024;
    var ctx = c.getContext("2d");
    var g = ctx.createRadialGradient(512, 420, 40, 512, 480, 480);
    g.addColorStop(0, "rgba(40,220,200,0.55)");
    g.addColorStop(0.25, "rgba(80,160,255,0.22)");
    g.addColorStop(0.55, "rgba(255,120,60,0.18)");
    g.addColorStop(0.85, "rgba(255,200,120,0.08)");
    g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 1024, 1024);
    var tex = new THREE.CanvasTexture(c);
    tex.needsUpdate = true;
    return tex;
  }

  function makeNebulaTextureWarm() {
    var c = document.createElement("canvas");
    c.width = 1024;
    c.height = 1024;
    var ctx = c.getContext("2d");
    var g = ctx.createRadialGradient(380, 360, 20, 520, 520, 520);
    g.addColorStop(0, "rgba(255,200,120,0.5)");
    g.addColorStop(0.2, "rgba(255,120,60,0.28)");
    g.addColorStop(0.45, "rgba(200,80,180,0.16)");
    g.addColorStop(0.75, "rgba(40,100,200,0.1)");
    g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 1024, 1024);
    var tex = new THREE.CanvasTexture(c);
    tex.needsUpdate = true;
    return tex;
  }

  var nebTex = makeNebulaTexture();
  var nebula = new THREE.Mesh(
    new THREE.SphereGeometry(42000, 48, 48),
    new THREE.MeshBasicMaterial({
      map: nebTex,
      side: THREE.BackSide,
      transparent: true,
      opacity: 0.55,
      depthWrite: false,
    })
  );
  nebula.position.set(-8000, 2000, -24000);
  scene.add(nebula);

  var nebTexWarm = makeNebulaTextureWarm();
  var nebulaWarm = new THREE.Mesh(
    new THREE.SphereGeometry(38000, 40, 40),
    new THREE.MeshBasicMaterial({
      map: nebTexWarm,
      side: THREE.BackSide,
      transparent: true,
      opacity: 0.38,
      depthWrite: false,
    })
  );
  nebulaWarm.position.set(12000, -1200, 18000);
  scene.add(nebulaWarm);

  var starCount = 24000;
  var positions = new Float32Array(starCount * 3);
  var colors = new Float32Array(starCount * 3);
  for (var i = 0; i < starCount; i++) {
    var R = 16000 + Math.random() * 42000;
    var u = Math.random() * 2 - 1;
    var t = Math.random() * Math.PI * 2;
    var s = Math.sqrt(1 - u * u);
    positions[i * 3] = Math.cos(t) * s * R;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 9000;
    positions[i * 3 + 2] = Math.sin(t) * s * R;
    var warm = Math.random();
    if (warm > 0.86) {
      colors[i * 3] = 1;
      colors[i * 3 + 1] = 0.85 + Math.random() * 0.12;
      colors[i * 3 + 2] = 0.65;
    } else if (warm > 0.55) {
      colors[i * 3] = 0.75 + Math.random() * 0.2;
      colors[i * 3 + 1] = 0.88 + Math.random() * 0.1;
      colors[i * 3 + 2] = 1;
    } else {
      colors[i * 3] = 0.88 + Math.random() * 0.1;
      colors[i * 3 + 1] = 0.9 + Math.random() * 0.08;
      colors[i * 3 + 2] = 1;
    }
  }
  var starGeo = new THREE.BufferGeometry();
  starGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  starGeo.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  var stars = new THREE.Points(
    starGeo,
    new THREE.PointsMaterial({ size: 1.35, vertexColors: true, transparent: true, opacity: 0.92, depthWrite: false, sizeAttenuation: true })
  );
  scene.add(stars);

  scene.add(new THREE.AmbientLight(0x1a2030, 0.28));
  scene.add(new THREE.HemisphereLight(0x224466, 0x080410, 0.45));
  var sunLight = new THREE.PointLight(0xffccaa, 3.2, 0, 2);
  sunLight.position.set(0, 0, 0);
  scene.add(sunLight);
  var rimLight = new THREE.DirectionalLight(0x66ccff, 0.35);
  rimLight.position.set(-1, 0.4, 1);
  scene.add(rimLight);

  var system = new THREE.Group();
  system.rotation.x = -1.12;
  system.rotation.z = 0.06;
  scene.add(system);

  function makeLabelSprite(text, borderHex, scaleW, scaleH) {
    var c = document.createElement("canvas");
    c.width = 512;
    c.height = 128;
    var ctx = c.getContext("2d");
    ctx.fillStyle = "rgba(6,10,24,0.82)";
    ctx.fillRect(4, 4, 504, 120);
    ctx.strokeStyle = borderHex || "#44ddcc";
    ctx.lineWidth = 3;
    ctx.strokeRect(4, 4, 504, 120);
    ctx.font = "bold 44px Rajdhani, Arial, sans-serif";
    ctx.fillStyle = "#f4f8ff";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(text, 256, 64);
    var tex = new THREE.CanvasTexture(c);
    tex.needsUpdate = true;
    var mat = new THREE.SpriteMaterial({ map: tex, transparent: true, depthWrite: false, opacity: 0.95 });
    var sp = new THREE.Sprite(mat);
    sp.scale.set(scaleW || 520, scaleH || 130, 1);
    return sp;
  }

  var sunMesh = new THREE.Mesh(
    new THREE.SphereGeometry(118, 64, 64),
    new THREE.MeshStandardMaterial({
      color: 0xffaa44,
      emissive: 0xff5500,
      emissiveIntensity: 0.85,
      roughness: 0.45,
      metalness: 0.15,
    })
  );
  system.add(sunMesh);
  var corona = new THREE.Mesh(
    new THREE.SphereGeometry(460, 32, 32),
    new THREE.MeshBasicMaterial({ color: 0xff6610, transparent: true, opacity: 0.14, depthWrite: false })
  );
  system.add(corona);

  var lylaLabel = makeLabelSprite("LYLA", "#2dd4bf", 620, 150);
  lylaLabel.position.set(0, 200, 0);
  system.add(lylaLabel);

  var AU = 520;
  var refAU = 1.0;
  var refPeriod = 55;
  function periodSec(au) {
    return refPeriod * Math.pow(Math.max(0.18, au) / refAU, 1.5);
  }

  var planetDefs = [
    { au: 0.42, size: 16, color: 0xff8866, name: "VEGA", ring: false },
    { au: 0.72, size: 14, color: 0xaa77ff, name: "FATE", ring: false },
    { au: 1.02, size: 20, color: 0x44aaee, name: "GOVERNANCE", ring: true },
    { au: 1.38, size: 15, color: 0x33ddaa, name: "WATERLINE", ring: false },
    { au: 1.78, size: 17, color: 0xffcc66, name: "DRIFTZERO", ring: false },
    { au: 2.18, size: 13, color: 0x88eeff, name: "CHOICE", ring: false },
    { au: 2.62, size: 14, color: 0xff4466, name: "COLLAPSE", ring: false },
  ];

  var bodies = [];
  planetDefs.forEach(function (pd, idx) {
    var anchor = new THREE.Object3D();
    anchor.rotation.x = (idx * 0.11 - 0.33) * 0.9;
    system.add(anchor);
    var dist = pd.au * AU;
    var mat = new THREE.MeshStandardMaterial({
      color: pd.color,
      roughness: 0.72,
      metalness: 0.12,
      emissive: new THREE.Color(pd.color).multiplyScalar(0.06),
    });
    var mesh = new THREE.Mesh(new THREE.SphereGeometry(pd.size, 36, 36), mat);
    mesh.position.set(dist, 0, 0);
    anchor.add(mesh);

    var lab = makeLabelSprite(pd.name, "#" + ("000000" + new THREE.Color(pd.color).getHex().toString(16)).slice(-6), 480, 120);
    lab.position.set(0, pd.size + 42, 0);
    mesh.add(lab);

    if (pd.ring) {
      var ring = new THREE.Mesh(
        new THREE.RingGeometry(pd.size * 2.1, pd.size * 3.6, 64),
        new THREE.MeshBasicMaterial({
          color: 0xc8b8ff,
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 0.55,
        })
      );
      ring.rotation.x = Math.PI / 2;
      mesh.add(ring);
    }

    bodies.push({
      type: "planet",
      anchor: anchor,
      mesh: mesh,
      dist: dist,
      period: periodSec(pd.au),
      angle: Math.random() * Math.PI * 2,
      tilt: (Math.random() - 0.5) * 0.08,
    });
  });

  planetDefs.forEach(function (pd) {
    var d = pd.au * AU;
    var curve = new THREE.EllipseCurve(0, 0, d, d, 0, Math.PI * 2, false, 0);
    var pts = curve.getPoints(200);
    var geo = new THREE.BufferGeometry().setFromPoints(pts.map(function (p) { return new THREE.Vector3(p.x, 0, p.y); }));
    var line = new THREE.Line(
      geo,
      new THREE.LineBasicMaterial({ color: 0xaaccff, transparent: true, opacity: 0.13 })
    );
    line.rotation.x = Math.PI / 2;
    system.add(line);
  });

  var t0 = performance.now();
  function animate(now) {
    var t = (now - t0) / 1000;
    var dt = 1 / 60;

    stars.rotation.y += 0.00001;
    nebula.rotation.y += 0.000006;
    nebulaWarm.rotation.y -= 0.000004;
    nebulaWarm.rotation.x += 0.000002;

    bodies.forEach(function (b) {
      if (b.type === "planet") {
        var omega = (Math.PI * 2) / b.period;
        b.angle += omega * dt;
        b.anchor.rotation.z = b.tilt * Math.sin(t * 0.07 + b.angle);
        b.anchor.rotation.y = b.angle;
      }
    });

    sunMesh.rotation.y += 0.0009;
    corona.rotation.y -= 0.00022;
    lylaLabel.position.y = 190 + Math.sin(t * 0.6) * 12;

    var camR = 5600 + Math.sin(t * 0.06) * 260;
    var camH = 5200 + Math.sin(t * 0.09) * 180;
    var camA = t * 0.028;
    camera.position.set(Math.sin(camA) * camR * 0.82, camH, Math.cos(camA) * camR * 0.82);
    camera.lookAt(0, -120, 0);

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);
})();
