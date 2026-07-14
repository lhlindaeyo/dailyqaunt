// 탭 라우팅: 사이드바 아이콘 클릭 → 해당 섹션 표시
const CONFIG_URL = "./data/config.json";

// 전역으로 config 공유 (각 탭 스크립트가 사용)
window.APP = { config: null };

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
  location.hash = tab;
}

document.querySelectorAll(".nav-btn").forEach((btn) => {
  btn.addEventListener("click", () => switchTab(btn.dataset.tab));
});

// 새로고침 시 해시 유지
window.addEventListener("DOMContentLoaded", () => {
  const tab = (location.hash || "#home").slice(1);
  if (document.getElementById("tab-" + tab)) switchTab(tab);
  loadConfig();
});
