"""
팩터 IC / 수익률 분석
- IC(Information Coefficient): 팩터 스코어와 다음 기간 수익률의 순위상관
- 퀀타일 포트폴리오 수익률 분석
사용 예:
    python research/alpha/factor_analysis.py
TODO: alphalens-reloaded 연동
"""
import pandas as pd


def information_coefficient(factor: pd.DataFrame, fwd_return: pd.DataFrame) -> pd.Series:
    """기간별 스피어만 순위상관(IC) 시계열 반환."""
    ic = {}
    for date in factor.index:
        f = factor.loc[date].dropna()
        r = fwd_return.loc[date].reindex(f.index).dropna()
        common = f.index.intersection(r.index)
        if len(common) > 2:
            ic[date] = f[common].corr(r[common], method="spearman")
    return pd.Series(ic, name="IC")


if __name__ == "__main__":
    print("팩터 분석 모듈 — 상위 파이프라인에서 import 하여 사용하세요.")
