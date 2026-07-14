"""백테스팅 실행 페이지 (뼈대). 실제 엔진 로직을 run_backtest()에 채우세요."""
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Backtest", page_icon="📈", layout="wide")
st.title("📈 백테스팅")

col1, col2, col3 = st.columns(3)
with col1:
    universe = st.selectbox("유니버스", ["KOSPI200", "KOSDAQ150", "S&P500"])
with col2:
    factor = st.selectbox("팩터", ["PER", "PBR", "ROE", "Momentum"])
with col3:
    rebal = st.selectbox("리밸런싱", ["월", "분기", "반기"])

start, end = st.columns(2)
start_date = start.date_input("시작일", value=pd.to_datetime("2018-01-01"))
end_date = end.date_input("종료일", value=pd.to_datetime("2025-12-31"))


def run_backtest(universe, factor, rebal, start_date, end_date):
    """TODO: 실제 백테스트 엔진 연결. 지금은 더미 수익률 곡선."""
    idx = pd.date_range(start_date, end_date, freq="B")
    rng = np.random.default_rng(42)
    rets = rng.normal(0.0004, 0.01, len(idx))
    equity = pd.Series((1 + rets).cumprod(), index=idx, name="Equity")
    cagr = equity.iloc[-1] ** (252 / len(equity)) - 1
    mdd = (equity / equity.cummax() - 1).min()
    sharpe = rets.mean() / rets.std() * np.sqrt(252)
    return equity, {"CAGR": cagr, "MDD": mdd, "Sharpe": sharpe}


if st.button("백테스트 실행", type="primary"):
    equity, stats = run_backtest(universe, factor, rebal, start_date, end_date)
    st.line_chart(equity)
    m1, m2, m3 = st.columns(3)
    m1.metric("CAGR", f"{stats['CAGR']*100:.1f}%")
    m2.metric("MDD", f"{stats['MDD']*100:.1f}%")
    m3.metric("Sharpe", f"{stats['Sharpe']:.2f}")
