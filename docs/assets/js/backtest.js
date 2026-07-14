// 백테스팅: Find Alpha = 팩터별 백테스트 결과 목록(클릭 시 아래 패널에 결과 글 렌더)
// 파란도형 = 새 백테스팅 Streamlit 링크
document.addEventListener("config:ready", () => {
  const cfg = window.APP.config || {};
  const bt = cfg.backtest || {};

  const list = document.getElementById("alpha-list");
  const body = document.getElementById("backtest-body");
  const factors = bt.factors || [];

  // 파란 도형 → 새 백테스팅 Streamlit URL
  const box = document.getElementById("new-backtest");
  box.href = bt.newBacktestUrl || "#";

  if (!factors.length) {
    list.innerHTML = "<li class='muted'>config.json의 backtest.factors에 항목을 추가하세요.</li>";
    body.innerHTML = "";
    return;
  }

  list.innerHTML = "";
  factors.forEach((f, i) => {
    const li = document.createElement("li");
    li.className = "alpha-item" + (i === 0 ? " active" : "");
    li.innerHTML = `
      <span class="dot"></span>
      <span class="alpha-name">${f.name}</span>
      <span class="alpha-result">${f.result || ""}</span>`;
    li.addEventListener("click", () => {
      list.querySelectorAll(".alpha-item").forEach((el) => el.classList.remove("active"));
      li.classList.add("active");
      renderFactor(f, body);
    });
    list.appendChild(li);
  });

  renderFactor(factors[0], body); // 첫 팩터 기본 표시
});

async function renderFactor(f, el) {
  el.innerHTML = "<p class='muted'>불러오는 중…</p>";
  try {
    const res = await fetch("./content/backtests/" + f.file);
    if (!res.ok) throw new Error("not found");
    const md = await res.text();
    el.innerHTML = marked.parse(md);
  } catch (e) {
    el.innerHTML = `<p class='muted'>결과 글이 아직 없어요. <code>docs/content/backtests/${f.file}</code> 파일을 작성해 커밋하세요.</p>`;
  }
}
