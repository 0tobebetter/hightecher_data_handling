# htmlxls-to-xlsx-converter-app/Home.py
import streamlit as st

st.subheader("📊 데이터를 다루자")

st.markdown(
    """
    <div style='text-align: center; background-color: #fdf6e3; padding: 1em; border-radius: 12px; font-size: 24px;'>
        ♪٩(٩ •'ᵕ'• ) "✧♪( •'ᵕ'•و(و "✧
    </div>
    <p style='text-align: right; font-size: 8pt;'>관리: 마케팅팀 박소정 매니저</p>
    """,
    unsafe_allow_html=True
)

st.markdown("""
👈 왼쪽 사이드바에서 사용할 기능을 선택하세요.

1. **xls파일들을 xlsx로 변환**
- `.xls` → `.xlsx` 변환
2. **xlsx파일 합치기**
- `.xlsx` 파일 헤더 기준 통합 

""")

st.info("Python, Pandas, Streamlit, Streamlit Cloud 이용 (서버에 파일 저장 X)")
