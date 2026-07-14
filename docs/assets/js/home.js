// 홈: macro.json(9개 지표 × 7일)을 읽어 카드 + 7일치 표 렌더
const MACRO_URL = "./data/macro.json";

async function loadMacro() {
  const grid = document.getElementById("home-grid");
  const detail = document.getElementById("home-detail");
  const updated = document.getElementById("home-updated");
  grid.innerHTML = "<p class='muted'>불러오는 중…</p>";

  try {
    // 캐시 방지용 쿼리스트링 → "run" 시 최신 JSON을 강제로 다시 받음
    const res = await fetch(MACRO_URL + "?t=" + Date.now());
    const data = await res.json();
    updated.textContent = "기준일: " + (data.generated || "-");

    // 카드 (마지막 값 + 전일 대비, 분기 지표는 발표 시점 배지로 대체)
    grid.innerHTML = "";
    data.series.forEach((s) => {
      const v = s.values;
      const last = v[v.length - 1];
      const card = document.createElement("div");
      card.className = "metric-card";

      if (s.freq === "quarterly") {
        card.innerHTML = `
          <div class="name">${s.name}</div>
          <div class="value">${fmt(last, s.unit)}</div>
          <div class="chg quarterly">${s.asOf || "분기"} 발표치 · 매일 갱신 아님</div>`;
      } else {
        const prev = v[v.length - 2] ?? last;
        const chg = last - prev;
        const pct = prev ? ((chg / prev) * 100).toFixed(2) : "0.00";
        const dir = chg >= 0 ? "up" : "down";
        card.innerHTML = `
          <div class="name">${s.name}</div>
          <div class="value">${fmt(last, s.unit)}</div>
          <div class="chg ${dir}">${chg >= 0 ? "▲" : "▼"} ${Math.abs(chg).toFixed(2)} (${pct}%)</div>`;
      }
      grid.appendChild(card);
    });

    // 7일치 표
    renderTable(detail, data);
  } catch (e) {
    grid.innerHTML = "<p class='muted'>데이터가 아직 없어요. GitHub Actions가 macro.json을 생성하면 표시됩니다.</p>";
    console.error(e);
  }
}

function fmt(n, unit) {
  const s = Number(n).toLocaleString("ko-KR");
  return unit ? `${s} ${unit}` : s;
}

function renderTable(el, data) {
  const days = data.dates || [];
  let html = "<table><thead><tr><th>지표</th>";
  days.forEach((d) => (html += `<th>${d.slice(5)}</th>`));
  html += "</tr></thead><tbody>";
  data.series.forEach((s) => {
    html += `<tr><td>${s.name}</td>`;
    s.values.forEach((v) => (html += `<td>${Number(v).toLocaleString("ko-KR")}</td>`));
    html += "</tr>";
  });
  html += "</tbody></table>";
  el.innerHTML = html;
}

document.getElementById("home-run").addEventListener("click", loadMacro);
document.addEventListener("DOMContentLoaded", loadMacro);
