// static/ai_thinking.js
(function () {
  const el = () => window.KD.byId("thinking");
  let dots = 0;
  let timer = null;

  function start() {
    if (timer) return;
    timer = setInterval(() => {
      const node = el();
      if (!node) return;
      dots = (dots + 1) % 4;
      node.textContent = "Thinking" + ".".repeat(dots);
    }, 450);
  }

  function stop() {
    if (timer) clearInterval(timer);
    timer = null;
    dots = 0;
  }

  window.addEventListener("KD:response", () => {
    stop();
  });

  document.addEventListener("DOMContentLoaded", () => {
    start();
  });
})();
