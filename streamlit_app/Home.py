"""
Streamlit 멀티페이지 앱 진입점.
Streamlit Community Cloud에 이 폴더(streamlit_app)를 배포하고,
Main file path 를 streamlit_app/Home.py 로 지정하세요.

배포 후 나오는 URL을 docs/data/config.json 의
targetMethods[].url 및 backtest.newBacktestUrl 에 넣으면
GitHub Pages 프론트에서 연결됩니다.
"""
import streamlit as st

st.set_page_config(page_title="Daily Quant · Tools", page_icon="$", layout="wide")

st.title("Daily Quant · 계산 도구")
st.write(
    "왼쪽 사이드바에서 페이지를 선택하세요. "
    "이 앱은 GitHub Pages 프론트엔드에서 링크로 연결됩니다."
)
st.page_link("pages/1_Backtest.py", label="백테스팅 실행", icon="📈")
st.page_link("pages/2_New_Backtest.py", label="새 백테스팅 만들기", icon="🧪")
st.page_link("pages/3_Target_Price.py", label="목표주가 계산", icon="🎯")
