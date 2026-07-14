"""새 백테스팅 생성 페이지 — 프론트의 '파란 도형'이 이 URL로 연결됩니다."""
import streamlit as st

st.set_page_config(page_title="New Backtest", page_icon="🧪", layout="wide")
st.title("🧪 새 백테스팅 만들기")

st.write("나만의 전략을 정의하고 백테스트를 생성하세요.")

name = st.text_input("전략 이름")
desc = st.text_area("전략 설명 / 규칙")
code = st.text_area("시그널 코드 (선택)", height=200, placeholder="def signal(df): ...")

if st.button("전략 저장", type="primary"):
    # TODO: 전략을 저장(파일/DB)하고 1_Backtest 에서 불러오도록 연결
    st.success(f"'{name}' 전략이 저장되었습니다. (저장 로직은 TODO)")
