// static/system.js
window.KD = window.KD || {};
window.KD.apiUrl = "/ENGINE";
window.KD.state = {};

window.KD.byId = (id) => document.getElementById(id);

window.KD.getValue = (id, fallback = "") => {
  const el = window.KD.byId(id);
  if (!el) return fallback;
  return el.value ?? fallback;
};

window.KD.setText = (id, value) => {
  const el = window.KD.byId(id);
  if (!el) return;
  el.textContent = value == null ? "" : String(value);
};

window.KD.setValue = (id, value) => {
  const el = window.KD.byId(id);
  if (!el) return;
  el.value = value == null ? "" : String(value);
};

window.KD.clamp = (value, low = 0, high = 100) => {
  const n = Number(value);
  if (!Number.isFinite(n)) return low;
  return Math.max(low, Math.min(high, n));
};

window.KD.readInputs = () => ({
  input: window.KD.getValue("input", ""),
  entropy: Number(window.KD.getValue("entropy", 40)) || 40,
  resource: Number(window.KD.getValue("resource", 50)) || 50,
  stability: Number(window.KD.getValue("stability", 60)) || 60,
  choices: Number(window.KD.getValue("choices", 1)) || 1,
  confidence: Number(window.KD.getValue("confidence", 0.5)) || 0.5,
});

window.KD.writeJSON = (id, value) => {
  window.KD.setText(id, JSON.stringify(value, null, 2));
};

window.KD.setState = (nextState) => {
  window.KD.state = nextState || {};
  window.dispatchEvent(new CustomEvent("KD:response", { detail: window.KD.state }));
};

window.KD.resizeCanvas = (canvas) => {
  if (!canvas) return null;
  const dpr = window.devicePixelRatio || 1;
  const width = Math.floor(window.innerWidth * dpr);
  const height = Math.floor(window.innerHeight * dpr);
  canvas.width = width;
  canvas.height = height;
  canvas.style.width = "100%";
  canvas.style.height = "100%";
  const ctx = canvas.getContext("2d");
  if (ctx) ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return ctx;
};

window.KD.bind = (id, event, handler) => {
  const el = window.KD.byId(id);
  if (!el) return;
  el.addEventListener(event, handler);
};
