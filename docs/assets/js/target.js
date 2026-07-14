// 목표주가: 계산법 가로칩 → 선택 시 설명 + Streamlit 계산 페이지 링크
document.addEventListener("config:ready", () => {
  const cfg = window.APP.config || {};
  const chips = document.getElementById("target-chips");
  const body = document.getElementById("target-body");
  const methods = cfg.targetMethods || [];

  if (!methods.length) {
    chips.innerHTML = "<p class='muted'>config.json에 targetMethods를 추가하세요.</p>";
    return;
  }

  methods.forEach((m, i) => {
    const chip = document.createElement("div");
    chip.className = "chip" + (i === 0 ? " active" : "");
    chip.innerHTML = `<div class="chip-title">${m.name}</div>
                      <div class="chip-sub">${m.sub || ""}</div>`;
    chip.addEventListener("click", () => {
      chips.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
      renderMethod(m, body);
    });
    chips.appendChild(chip);
  });

  renderMethod(methods[0], body);
});

function renderMethod(m, el) {
  el.innerHTML = `
    <h2>${m.name}</h2>
    <p>${m.desc || ""}</p>
    <a class="link-btn" href="${m.url || "#"}" target="_blank" rel="noopener">
      ${m.name} 계산기 열기 (Streamlit)
    </a>`;
}
