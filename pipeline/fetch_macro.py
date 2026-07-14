"""
홈 대시보드용 매크로 데이터 수집기.
GitHub Actions에서 실행되어 docs/data/macro.json 을 생성한다.
최근 7 거래일치의 지표를 받아와 프론트(home.js)가 읽을 형태로 저장.
GDP는 분기 지표라 매일 값이 없으므로, 최신 발표치를 7일 슬롯에 forward-fill 하고
freq/asOf 필드로 "분기 데이터"임을 표시한다.

로컬 테스트:  python pipeline/fetch_macro.py
필요 환경변수: FRED_API_KEY (GDP 수집용, https://fred.stlouisfed.org/docs/api/api_key.html 에서 무료 발급)
"""
import json
import os
import datetime as dt
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    import requests
except ImportError:
    requests = None

OUT = Path(__file__).resolve().parent.parent / "docs" / "data" / "macro.json"

# (id, 표시이름, 단위, yfinance 티커)
SERIES = [
    ("usdkrw", "원/달러",   "원", "KRW=X"),
    ("usdjpy", "엔/달러",   "",   "JPY=X"),
    ("kospi",  "KOSPI",    "",   "^KS11"),
    ("kosdaq", "KOSDAQ",   "",   "^KQ11"),
    ("sp500",  "S&P 500",  "",   "^GSPC"),
    ("nasdaq", "NASDAQ",   "",   "^IXIC"),
    ("us10y",  "美 10년물", "%",  "^TNX"),
    ("wti",    "WTI 유가",  "$",  "CL=F"),
    ("gold",   "금 (온스)", "$",  "GC=F"),
]

# 美 실질GDP 성장률(전기대비 연율, %) — FRED series id
FRED_GDP_SERIES_ID = "A191RL1Q225SBEA"


def fetch():
    """yfinance로 최근 7 거래일 종가를 받아온다."""
    dates_set = set()
    rows = []
    for sid, name, unit, ticker in SERIES:
        hist = yf.Ticker(ticker).history(period="10d")["Close"].dropna().tail(7)
        vals = [round(float(v), 2) for v in hist.values]
        idx = [d.strftime("%Y-%m-%d") for d in hist.index]
        dates_set.update(idx)
        rows.append({"id": sid, "name": name, "unit": unit, "values": vals, "_dates": idx})

    dates = sorted(dates_set)[-7:]
    series = [{"id": r["id"], "name": r["name"], "unit": r["unit"], "values": r["values"]} for r in rows]
    return dates, series


def fetch_gdp(dates):
    """FRED에서 최신 GDP 성장률을 받아 dates 개수만큼 forward-fill 한다."""
    api_key = os.environ.get("FRED_API_KEY")
    if not api_key or requests is None:
        print("FRED_API_KEY 미설정 또는 requests 미설치 → GDP 카드 생략")
        return None

    url = (
        "https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={FRED_GDP_SERIES_ID}&api_key={api_key}&file_type=json"
        "&sort_order=desc&limit=1"
    )
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        obs = res.json()["observations"][0]
        value = round(float(obs["value"]), 2)
        quarter_label = _to_quarter_label(obs["date"])
    except Exception as e:
        print(f"GDP 수집 실패: {e}")
        return None

    return {
        "id": "gdp",
        "name": "美 실질GDP 성장률",
        "unit": "%",
        "freq": "quarterly",
        "asOf": quarter_label,
        "values": [value] * len(dates),
    }


def _to_quarter_label(date_str):
    d = dt.date.fromisoformat(date_str)
    q = (d.month - 1) // 3 + 1
    return f"{d.year}Q{q}"


def main():
    if yf is None:
        raise SystemExit("yfinance 미설치: pip install -r pipeline/requirements.txt")
    dates, series = fetch()

    gdp = fetch_gdp(dates)
    if gdp:
        series.append(gdp)

    data = {
        "generated": dt.date.today().isoformat(),
        "dates": dates,
        "series": series,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"저장 완료: {OUT}  ({len(series)}개 지표)")


if __name__ == "__main__":
    main()
