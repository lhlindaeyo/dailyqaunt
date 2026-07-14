"""
추세 보조지표: MACD, EMA, SMA, 볼린저밴드
사용 예:
    python research/indicators/trend.py --ticker 005930
입력: output/stock_<ticker>.csv  →  출력: output/indicators_trend_<ticker>.csv
"""
import argparse
import os
import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")


def add_trend(df: pd.DataFrame) -> pd.DataFrame:
    close = df["close"]
    df["sma20"] = close.rolling(20).mean()
    df["sma60"] = close.rolling(60).mean()
    df["ema12"] = close.ewm(span=12, adjust=False).mean()
    df["ema26"] = close.ewm(span=26, adjust=False).mean()
    df["macd"] = df["ema12"] - df["ema26"]
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]
    ma20 = close.rolling(20).mean()
    std20 = close.rolling(20).std()
    df["bb_upper"] = ma20 + 2 * std20
    df["bb_lower"] = ma20 - 2 * std20
    return df


def main():
    p = argparse.ArgumentParser(description="추세 보조지표 계산")
    p.add_argument("--ticker", required=True)
    args = p.parse_args()

    src = os.path.join(OUTPUT_DIR, f"stock_{args.ticker}.csv")
    df = pd.read_csv(src, index_col=0, parse_dates=True)
    df = add_trend(df)
    out = os.path.join(OUTPUT_DIR, f"indicators_trend_{args.ticker}.csv")
    df.to_csv(out)
    print(f"저장 완료: {out}")


if __name__ == "__main__":
    main()
