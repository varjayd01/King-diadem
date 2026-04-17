// static/galaxy_decision.js
function renderGalaxyDecision(payload) {
  const target = window.KD.byId("summary");
  if (!target) return;

  const output = payload?.output || {};
  const consensus = payload?.consensus || {};

  const lines = [
    `final_action: ${output.action || consensus.final_action || "n/a"}`,
    `risk: ${output.risk ?? payload?.risk?.risk_score ?? "n/a"}`,
    `confidence: ${output.confidence ?? consensus.confidence ?? "n/a"}`,
    `reason: ${output.reason || "clear"}`,
  ];

  target.textContent = lines.join(" | ");
}

window.renderGalaxyDecision = renderGalaxyDecision;

window.addEventListener("KD:response", (event) => {
  renderGalaxyDecision(event.detail);
});
