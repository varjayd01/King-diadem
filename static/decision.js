// static/dicision.js
window.renderDicision = function (payload) {
  if (typeof window.renderDecision === "function") {
    window.renderDecision(payload);
  }
};
