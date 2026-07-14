"""
모멘텀 보조지표: RSI, Stochastic, ROC
사용 예:
    python research/indicators/momentum.py --ticker 005930
"""
import argparse
import os
import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")


def add_momentum(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    close = df["close"]
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    low_n = df["low"].rolling(period).min()
    high_n = df["high"].rolling(period).max()
    df["stoch_k"] = 100 * (close - low_n) / (high_n - low_n)
    df["stoch_d"] = df["stoch_k"].rolling(3).mean()

    df["roc"] = close.pct_change(period) * 100
    return df


def main():
    p = argparse.ArgumentParser(description="모멘텀 보조지표 계산")
    p.add_argument("--ticker", required=True)
    args = p.parse_args()
    src = os.path.join(OUTPUT_DIR, f"stock_{args.ticker}.csv")
    df = add_momentum(pd.read_csv(src, index_col=0, parse_dates=True))
    out = os.path.join(OUTPUT_DIR, f"indicators_momentum_{args.ticker}.csv")
    df.to_csv(out)
    print(f"저장 완료: {out}")


if __name__ == "__main__":
    main()
