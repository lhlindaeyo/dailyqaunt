"""
종목 차트 데이터 → JSON 변환 (TradingView Lightweight Charts 포맷)
사용 예:
    python research/export/export_chart.py --ticker 005930
입력: output/indicators_trend_<ticker>.csv (없으면 stock_<ticker>.csv)
출력: site/data/chart_<ticker>.json
"""
import argparse
import json
import os
import pandas as pd

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUTPUT_DIR = os.path.join(ROOT, "output")
SITE_DATA = os.path.join(ROOT, "site", "data")


def main():
    p = argparse.ArgumentParser(description="차트 JSON 변환")
    p.add_argument("--ticker", required=True)
    args = p.parse_args()

    trend = os.path.join(OUTPUT_DIR, f"indicators_trend_{args.ticker}.csv")
    src = trend if os.path.exists(trend) else os.path.join(
        OUTPUT_DIR, f"stock_{args.ticker}.csv")
    df = pd.read_csv(src, index_col=0, parse_dates=True)

    def series(col):
        return [{"time": t.strftime("%Y-%m-%d"), "value": round(float(v), 4)}
                for t, v in df[col].dropna().items()] if col in df else []

    candles = [{"time": t.strftime("%Y-%m-%d"),
                "open": float(r.open), "high": float(r.high),
                "low": float(r.low), "close": float(r.close)}
               for t, r in df.iterrows()]

    payload = {
        "ticker": args.ticker,
        "candles": candles,
        "volume": [{"time": t.strftime("%Y-%m-%d"), "value": float(v)}
                   for t, v in df["volume"].items()],
        "indicators": {k: series(k) for k in
                       ["sma20", "sma60", "bb_upper", "bb_lower", "rsi", "macd"]},
    }

    os.makedirs(SITE_DATA, exist_ok=True)
    out = os.path.join(SITE_DATA, f"chart_{args.ticker}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    print(f"저장 완료: {out}")


if __name__ == "__main__":
    main()
