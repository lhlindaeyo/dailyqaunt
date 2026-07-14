// 산업분석: config.industries의 가로칩 → 클릭 시 해당 .md fetch → marked 렌더
document.addEventListener("config:ready", () => {
  const cfg = window.APP.config || {};
  const chips = document.getElementById("industry-chips");
  const body = document.getElementById("industry-body");
  const industries = cfg.industries || [];

  if (!industries.length) {
    chips.innerHTML = "<p class='muted'>config.json에 industries를 추가하세요.</p>";
    return;
  }

  industries.forEach((ind, i) => {
    const chip = document.createElement("div");
    chip.className = "chip" + (i === 0 ? " active" : "");
    chip.innerHTML = `<div class="chip-title">${ind.name}</div>
                      <div class="chip-sub">${ind.sub || ""}</div>`;
    chip.addEventListener("click", () => {
      chips.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
      renderIndustry(ind, body);
    });
    chips.appendChild(chip);
  });

  renderIndustry(industries[0], body); // 첫 산업 기본 표시
});

async function renderIndustry(ind, el) {
  el.innerHTML = "<p class='muted'>불러오는 중…</p>";
  try {
    const res = await fetch("./content/industries/" + ind.file);
    if (!res.ok) throw new Error("not found");
    const md = await res.text();
    el.innerHTML = marked.parse(md);
  } catch (e) {
    el.innerHTML = `<p class='muted'>글이 아직 없어요. <code>docs/content/industries/${ind.file}</code> 파일을 작성해 커밋하세요.</p>`;
  }
}
