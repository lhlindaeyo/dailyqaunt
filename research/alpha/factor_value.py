"""가치 팩터: PER, PBR 기반 팩터 스코어 (낮을수록 저평가)."""
import pandas as pd


def value_factor(fundamentals: pd.DataFrame) -> pd.Series:
    """
    fundamentals: columns=[per, pbr], index=티커
    PER/PBR 역수를 z-score로 합성한 밸류 스코어 반환.
    """
    earnings_yield = 1 / fundamentals["per"].replace(0, pd.NA)
    book_yield = 1 / fundamentals["pbr"].replace(0, pd.NA)
    z = lambda s: (s - s.mean()) / s.std()
    return z(earnings_yield).add(z(book_yield), fill_value=0)
