"""
거래량 보조지표: OBV, 거래량 이동평균
사용 예:
    python research/indicators/volume.py --ticker 005930
"""
import argparse
import os
import numpy as np
import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")


def add_volume(df: pd.DataFrame) -> pd.DataFrame:
    direction = np.sign(df["close"].diff()).fillna(0)
    df["obv"] = (direction * df["volume"]).cumsum()
    df["vol_ma20"] = df["volume"].rolling(20).mean()
    return df


def main():
    p = argparse.ArgumentParser(description="거래량 보조지표 계산")
    p.add_argument("--ticker", required=True)
    args = p.parse_args()
    src = os.path.join(OUTPUT_DIR, f"stock_{args.ticker}.csv")
    df = add_volume(pd.read_csv(src, index_col=0, parse_dates=True))
    out = os.path.join(OUTPUT_DIR, f"indicators_volume_{args.ticker}.csv")
    df.to_csv(out)
    print(f"저장 완료: {out}")


if __name__ == "__main__":
    main()
