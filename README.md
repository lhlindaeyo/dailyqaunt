# 📊 Daily Quant

개인 퀀트 리서치 플랫폼. **정적 프론트(GitHub Pages) + 데이터 파이프라인(GitHub Actions) + 계산 앱(Streamlit)** 3층 구조로 동작합니다.

- **프론트(`docs/`)** — 4개 탭 대시보드. GitHub Pages로 배포되는 순수 HTML/CSS/JS.
- **파이프라인(`pipeline/` + Actions)** — 매일 매크로 지표를 수집해 `docs/data/macro.json` 생성.
- **계산 앱(`streamlit_app/`)** — 백테스팅·목표주가 계산. Streamlit Community Cloud에 배포 후 프론트에서 링크로 연결.

---

## 📁 구조

```
dailyqaunt/
├── docs/                       # GitHub Pages (Settings → Pages → main /docs)
│   ├── index.html              # 4탭 SPA 껍데기
│   ├── assets/
│   │   ├── css/style.css        # 스크롤 스냅(가로) + 세로 스크롤
│   │   └── js/                  # app(라우팅) / home / industry / backtest / target
│   ├── data/
│   │   ├── macro.json           # 9개 지표(GDP 포함) × 7일 (Actions가 생성)
│   │   └── config.json          # 산업목록·계산법·Streamlit URL·백테스팅 팩터목록
│   └── content/
│       ├── industries/*.md      # 산업분석 글 (직접 작성)
│       └── backtests/*.md       # 팩터별 백테스트 결과 글 (직접 작성)
│
├── pipeline/
│   ├── fetch_macro.py           # yfinance(+FRED GDP) → docs/data/macro.json
│   └── requirements.txt
│
├── streamlit_app/               # Streamlit Cloud 배포 (main file: Home.py)
│   ├── Home.py
│   ├── pages/
│   │   ├── 1_Backtest.py
│   │   ├── 2_New_Backtest.py    # 프론트 '파란 도형' 링크 대상
│   │   └── 3_Target_Price.py    # ?method=per|dcf|rim 쿼리 분기
│   └── requirements.txt
│
├── research/                     # 로컬 전용 리서치/백테스트 엔진 (추후 streamlit_app과 연결 예정)
│
├── .env.example                  # FRED_API_KEY 등 로컬 환경변수 템플릿
└── .github/workflows/update-data.yml   # 매일 06:00 KST + 수동 실행
```

## 🧩 탭별 동작

| 탭 | 아이콘 | 동작 |
| --- | --- | --- |
| 홈 | ⌂ | 9개 지표 카드(GDP는 분기 배지로 표시) + **Run** 시 최근 7일치 표. 데이터는 Actions가 매일 자동 갱신, Run은 최신 캐시를 재조회 |
| 산업분석 | ⌕ | 가로 슬라이드로 산업 선택 → `content/industries/*.md` 렌더 |
| 백테스팅 | ▤ | Find Alpha(팩터별 백테스트 결과 요약) 클릭 → 하단에 해당 팩터의 결과 글 렌더 · 파란도형(새 백테스팅) → Streamlit |
| 목표주가 | ◈ | 가로 슬라이드로 계산법 선택 → Streamlit 계산기 |

## 🚀 세팅

**1. GitHub Pages 켜기** — Settings → Pages → Source: `main` 브랜치 `/docs` 폴더.

**2. Streamlit 배포** — [share.streamlit.io](https://share.streamlit.io) 에서 이 repo 연결, Main file path `streamlit_app/Home.py`. 배포 URL을 `docs/data/config.json` 의 `targetMethods[].url`·`backtest.newBacktestUrl` 에 입력.

**3. 데이터 자동화** — Actions 탭에서 `Update market data` 워크플로우 활성화. 즉시 실행하려면 `Run workflow` 클릭.
GDP 카드를 채우려면 저장소 Settings → Secrets and variables → Actions 에 `FRED_API_KEY`를 등록하세요 ([무료 발급](https://fred.stlouisfed.org/docs/api/api_key.html)). 키가 없으면 GDP 카드 없이 나머지 8개 지표만 갱신됩니다.

**4. 글 추가** — `docs/content/industries/`(산업분석) 또는 `docs/content/backtests/`(팩터별 백테스트 결과)에 `.md` 작성 → `config.json` 에 항목 추가 → 커밋.

## 🧪 로컬 테스트

```bash
pip install -r requirements.txt         # pipeline + streamlit_app 의존성 한 번에 설치
cp .env.example .env && $EDITOR .env    # FRED_API_KEY 입력 (선택)
python pipeline/fetch_macro.py          # macro.json 갱신
python -m http.server -d docs 8000      # http://localhost:8000 에서 프론트 확인
streamlit run streamlit_app/Home.py     # 계산 앱 확인
```

> 본 프로젝트는 투자 권유가 아니며 리서치/학습 목적입니다.
