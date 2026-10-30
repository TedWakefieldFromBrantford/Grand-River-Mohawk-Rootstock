(function () {
  const root = document.getElementById("quiz");
  if (!root) return;
  const cards = [...root.querySelectorAll(".card")];
  let i = 0;
  const sessionId = root.dataset.session;
  let t0 = performance.now();

  function show(n) {
    cards.forEach(c => c.style.display = "none");
    if (n >= cards.length) {
      document.getElementById("done").style.display = "block";
      return;
    }
    cards[n].style.display = "block";
    cards[n].querySelector(".given").focus();
    t0 = performance.now();
  }

  function bind(card) {
    const input = card.querySelector(".given");
    const btn = card.querySelector(".check");
    const fb = card.querySelector(".feedback");
    const submit = () => {
      const given = input.value;
      const answer = card.dataset.answer;
      fetch("/attempt", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          session_id: sessionId,
          item_id: 0,                        // stub; real item ids come later
          answer: answer,
          given: given,
          duration_ms: Math.round(performance.now() - t0)
        })
      }).then(r => r.json()).then(d => {
        fb.textContent = d.message;
        fb.className = "feedback " + (d.result === 2 ? "hit" : d.result === 1 ? "near" : "");
        btn.disabled = true;
        setTimeout(() => { i++; show(i); btn.disabled = false; input.value=""; fb.textContent=""; }, d.result === 2 ? 500 : 1600);
      });
    };
    btn.addEventListener("click", submit);
    input.addEventListener("keydown", e => { if (e.key === "Enter") submit(); });
  }

  cards.forEach(bind);
  show(0);
})();
