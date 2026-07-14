"""목표주가 계산 — 프론트에서 ?method=per|dcf|rim 쿼리로 진입."""
import streamlit as st

st.set_page_config(page_title="Target Price", page_icon="🎯", layout="wide")
st.title("🎯 목표주가 계산")

# 프론트 링크의 쿼리파라미터로 기본 계산법 선택
qp = st.query_params
default = qp.get("method", "per")
methods = {"per": "PER 밸류에이션", "dcf": "DCF", "rim": "잔여이익모형(RIM)"}
keys = list(methods.keys())
method = st.radio("계산법", keys, index=keys.index(default) if default in keys else 0,
                  format_func=lambda k: methods[k], horizontal=True)

st.divider()

if method == "per":
    eps = st.number_input("예상 EPS (원)", value=5000.0, step=100.0)
    per = st.number_input("목표 PER (배)", value=12.0, step=0.5)
    if st.button("계산", type="primary"):
        st.metric("적정주가", f"{eps * per:,.0f} 원")

elif method == "dcf":
    fcf = st.number_input("연간 FCF (억원)", value=1000.0, step=50.0)
    g = st.number_input("성장률 g (%)", value=3.0) / 100
    wacc = st.number_input("할인율 WACC (%)", value=9.0) / 100
    shares = st.number_input("발행주식수 (백만주)", value=100.0)
    if st.button("계산", type="primary"):
        if wacc > g:
            ev = fcf * (1 + g) / (wacc - g)          # 억원
            price = ev * 1e8 / (shares * 1e6)         # 원/주
            st.metric("주당 내재가치", f"{price:,.0f} 원")
        else:
            st.error("WACC는 성장률보다 커야 합니다.")

else:  # rim
    bps = st.number_input("주당순자산 BPS (원)", value=40000.0, step=500.0)
    roe = st.number_input("ROE (%)", value=12.0) / 100
    coe = st.number_input("자기자본비용 (%)", value=8.0) / 100
    if st.button("계산", type="primary"):
        price = bps * (1 + (roe - coe) / coe)
        st.metric("적정주가", f"{price:,.0f} 원")
