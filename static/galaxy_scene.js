// static/galaxy_scene.js — WebGL solar system (Three.js) · cockpit view with subtle camera orbit
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
  scene.fog = new THREE.FogExp2(0x020306, 0.00018);

  var camera = new THREE.PerspectiveCamera(48, 1, 10, 120000);
  camera.position.set(0, 520, 3200);

  function resize() {
    var w = window.innerWidth;
    var h = window.innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  resize();
  window.addEventListener("resize", resize);

  // —— Starfield (dense point cloud, NASA-ish depth) ——
  var starCount = 22000;
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

  var ambient = new THREE.AmbientLight(0x1a2030, 0.35);
  scene.add(ambient);
  var sunLight = new THREE.PointLight(0xffcc88, 2.4, 0, 2);
  sunLight.position.set(0, 0, 0);
  scene.add(sunLight);

  var system = new THREE.Group();
  scene.add(system);

  // Sun sphere + corona halo (mesh)
  var sunMesh = new THREE.Mesh(
    new THREE.SphereGeometry(110, 64, 64),
    new THREE.MeshBasicMaterial({ color: 0xffaa33 })
  );
  system.add(sunMesh);
  var corona = new THREE.Mesh(
    new THREE.SphereGeometry(420, 32, 32),
    new THREE.MeshBasicMaterial({ color: 0xff6610, transparent: true, opacity: 0.12, depthWrite: false })
  );
  system.add(corona);

  // Planets: mean distance AU-ish scale, period ∝ R^1.5 Kepler (inner faster)
  var AU = 520;
  var refAU = 1.0;
  var refPeriod = 60; // seconds per orbit for ~Earth distance
  function periodSec(au) {
    return refPeriod * Math.pow(Math.max(0.2, au) / refAU, 1.5);
  }
  var planetDefs = [
    { au: 0.38, size: 8, color: 0x8c8c8c, name: "Mercury" },
    { au: 0.72, size: 18, color: 0xc9a227, name: "Venus" },
    { au: 1.0, size: 20, color: 0x3366cc, name: "Earth", moon: true },
    { au: 1.4, size: 11, color: 0xcc5533, name: "Mars" },
    { au: 2.2, size: 34, color: 0xc4956a, name: "Jupiter" },
    { au: 2.85, size: 30, color: 0xd4b896, name: "Saturn", ring: true },
    { au: 3.5, size: 22, color: 0x66ccee, name: "Uranus" },
    { au: 4.2, size: 20, color: 0x4466cc, name: "Neptune" },
  ];

  var bodies = [];
  planetDefs.forEach(function (pd, idx) {
    var anchor = new THREE.Object3D();
    system.add(anchor);
    var dist = pd.au * AU;
    var mat = new THREE.MeshStandardMaterial({
      color: pd.color,
      roughness: 0.78,
      metalness: 0.08,
      emissive: new THREE.Color(pd.color).multiplyScalar(0.04),
    });
    var mesh = new THREE.Mesh(new THREE.SphereGeometry(pd.size, 36, 36), mat);
    mesh.position.set(dist, 0, 0);
    anchor.add(mesh);

    if (pd.ring) {
      var ring = new THREE.Mesh(
        new THREE.RingGeometry(pd.size * 2.1, pd.size * 3.6, 64),
        new THREE.MeshBasicMaterial({
          color: 0xd8c8a0,
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 0.5,
        })
      );
      ring.rotation.x = Math.PI / 2;
      mesh.add(ring);
    }

    if (pd.moon) {
      var moon = new THREE.Mesh(
        new THREE.SphereGeometry(3.2, 16, 16),
        new THREE.MeshStandardMaterial({ color: 0xbbbbbb, roughness: 0.9, metalness: 0 })
      );
      moon.position.set(pd.size + 28, 6, 0);
      mesh.add(moon);
      bodies.push({ type: "moon", mesh: moon, speed: 4.2 + idx * 0.1, ang: Math.random() * 6.28 });
    }

    bodies.push({
      type: "planet",
      anchor: anchor,
      mesh: mesh,
      dist: dist,
      period: periodSec(pd.au),
      angle: Math.random() * Math.PI * 2,
      tilt: (Math.random() - 0.5) * 0.16,
    });
  });

  // Thin orbit lines
  planetDefs.forEach(function (pd) {
    var d = pd.au * AU;
    var curve = new THREE.EllipseCurve(0, 0, d, d, 0, Math.PI * 2, false, 0);
    var pts = curve.getPoints(200);
    var geo = new THREE.BufferGeometry().setFromPoints(pts.map(function (p) { return new THREE.Vector3(p.x, 0, p.y); }));
    var line = new THREE.Line(
      geo,
      new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.06 })
    );
    line.rotation.x = Math.PI / 2;
    system.add(line);
  });

  var t0 = performance.now();
  function animate(now) {
    var t = (now - t0) / 1000;
    var dt = 1 / 60;

    stars.rotation.y += 0.000012;

    bodies.forEach(function (b) {
      if (b.type === "planet") {
        var omega = (Math.PI * 2) / b.period;
        b.angle += omega * dt;
        b.anchor.rotation.x = b.tilt;
        b.anchor.rotation.y = b.angle;
      } else if (b.type === "moon") {
        b.mesh.position.x = Math.cos(t * b.speed) * 34;
        b.mesh.position.z = Math.sin(t * b.speed) * 34;
      }
    });

    sunMesh.rotation.y += 0.0008;
    corona.rotation.y -= 0.00025;

    // Cockpit camera: very slow orbit + drift
    var camR = 3200 + Math.sin(t * 0.08) * 120;
    var camA = t * 0.052;
    camera.position.set(Math.sin(camA) * camR * 0.9, 480 + Math.sin(t * 0.11) * 90, Math.cos(camA) * camR);
    camera.lookAt(0, 0, 0);

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);
})();
