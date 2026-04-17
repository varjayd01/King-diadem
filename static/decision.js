// static/dicision.js
(function () {

  function renderDicision(payload) {
    const el = document.getElementById("decision");
    if (!el) return;

    // รองรับทุกโครงสร้างที่มึงโยนมา
    const d =
      payload?.decision ||
      payload?.output ||
      payload?.consensus ||
      payload ||
      {};

    const lines = [
      "status: " + (payload?.status || "ok"),
      "action: " + (d.action || d.final_action || "none"),
      "message: " + (d.message || "n/a"),
      "confidence: " + (d.confidence ?? "n/a"),
      "risk: " + (d.risk ?? payload?.risk_score ?? "n/a"),
      "blocked: " + (d.blocked ?? payload?.blocked ?? false)
    ];

    el.textContent = lines.join("\n");
  }

  // expose global
  window.renderDicision = renderDicision;

  // auto hook event (ถ้ามีระบบ dispatch)
  window.addEventListener("KD:response", function (e) {
    renderDicision(e.detail);
  });

})();
