import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.subheader("📂xlsx 파일 병합")
st.info("🍀첫 번째 파일의 헤더를 기준으로 병합됩니다.")

uploaded_files = st.file_uploader("📂여러 개의 .xlsx 파일을 업로드하세요", type=["xlsx"], accept_multiple_files=True)


if uploaded_files and len(uploaded_files) >= 2:

    try:
        # 첫 파일: 헤더 포함
        df_list = [pd.read_excel(uploaded_files[0], engine='openpyxl')]

        # 나머지 파일: 헤더 제거 후 첫 파일 기준으로 컬럼 맞추기
        for file in uploaded_files[1:]:
            df = pd.read_excel(file, header=None, skiprows=1, engine='openpyxl')
            df.columns = df_list[0].columns
            df_list.append(df)

        merged_df = pd.concat(df_list, ignore_index=True)

        # 다운로드용 Excel 변환
        towrite = BytesIO()
        merged_df.to_excel(towrite, index=False, engine="openpyxl")
        towrite.seek(0)

        today_str = datetime.today().strftime('%Y%m%d')
        st.download_button(
            label=f"📥 병합된 파일 다운로드 ({today_str})",
            data=towrite,
            file_name=f"merged_{today_str}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success("🎉 병합이 완료되었습니다!")

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
else:
    st.warning("최소 두 개의 파일을 업로드해주세요.")
