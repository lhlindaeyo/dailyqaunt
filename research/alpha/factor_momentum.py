"""모멘텀 팩터: 과거 N개월 수익률 기반 팩터 스코어."""
import pandas as pd


def momentum_factor(prices: pd.DataFrame, lookback: int = 120, skip: int = 20) -> pd.Series:
    """
    prices: 종목별 종가 (columns=티커, index=날짜)
    lookback 기간 수익률에서 최근 skip 기간을 제외한 모멘텀 스코어 반환.
    """
    return prices.shift(skip) / prices.shift(lookback) - 1
