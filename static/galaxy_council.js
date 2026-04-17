// static/galaxy_council.js
function renderCouncil(payload) {
  const target = window.KD.byId("council");
  if (!target) return;

  const council = payload?.council || {};
  const votes = Array.isArray(council.votes) ? council.votes : [];

  if (!votes.length) {
    target.textContent = "Waiting...";
    return;
  }

  const rows = votes.map((vote) => {
    return `${vote.member} (${vote.role}) -> ${vote.action} | ${vote.score}`;
  });

  rows.push("");
  rows.push(`council_score: ${council.score ?? "n/a"}`);

  target.textContent = rows.join("\n");
}

window.renderCouncil = renderCouncil;

window.addEventListener("KD:response", (event) => {
  renderCouncil(event.detail);
});
