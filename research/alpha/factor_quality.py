"""퀄리티 팩터: ROE, 부채비율 기반 팩터 스코어."""
import pandas as pd


def quality_factor(fundamentals: pd.DataFrame) -> pd.Series:
    """
    fundamentals: columns=[roe, debt_ratio], index=티커
    ROE는 높을수록, 부채비율은 낮을수록 좋음.
    """
    z = lambda s: (s - s.mean()) / s.std()
    return z(fundamentals["roe"]) - z(fundamentals["debt_ratio"])
