// 탭 라우팅 + 사이드바 접기/펼치기 + 상단 제목 동기화
const CONFIG_URL = "./data/config.json";

// 전역으로 config 공유 (각 탭 스크립트가 사용)
window.APP = { config: null };

const TAB_TITLES = {
  home: "Market Dashboard",
  industry: "Industry Research",
  backtest: "Backtesting",
  target: "Target Price",
};

async function loadConfig() {
  try {
    const res = await fetch(CONFIG_URL);
    window.APP.config = await res.json();
  } catch (e) {
    console.error("config.json 로드 실패", e);
    window.APP.config = {};
  }
  document.dispatchEvent(new Event("config:ready"));
}

function switchTab(tab) {
  document.querySelectorAll(".nav-btn").forEach((b) =>
    b.classList.toggle("active", b.dataset.tab === tab)
  );
  document.querySelectorAll(".tab").forEach((s) =>
    s.classList.toggle("active", s.id === "tab-" + tab)
  );
  const title = document.getElementById("page-title");
  if (title && TAB_TITLES[tab]) title.textContent = TAB_TITLES[tab];
  location.hash = tab;
}

document.querySelectorAll(".nav-btn").forEach((btn) => {
  btn.addEventListener("click", () => switchTab(btn.dataset.tab));
});

// ── 사이드바 접기/펼치기 (상태 localStorage 저장) ──
const COLLAPSE_KEY = "dq.sidebar.collapsed";
function setCollapsed(collapsed) {
  document.querySelector(".app").classList.toggle("collapsed", collapsed);
  localStorage.setItem(COLLAPSE_KEY, collapsed ? "1" : "0");
}
const collapseBtn = document.getElementById("collapse-btn");
if (collapseBtn) {
  collapseBtn.addEventListener("click", () =>
    setCollapsed(!document.querySelector(".app").classList.contains("collapsed"))
  );
}

// 초기화: 저장된 접힘 상태 + 해시 탭 복원
window.addEventListener("DOMContentLoaded", () => {
  if (localStorage.getItem(COLLAPSE_KEY) === "1")
    document.querySelector(".app").classList.add("collapsed");

  const tab = (location.hash || "#home").slice(1);
  if (document.getElementById("tab-" + tab)) switchTab(tab);
  loadConfig();
});
