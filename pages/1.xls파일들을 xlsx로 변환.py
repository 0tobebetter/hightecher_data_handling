
import streamlit as st
import pandas as pd
import zipfile
import os
from io import BytesIO
from datetime import datetime
from bs4 import BeautifulSoup
import chardet

st.set_page_config(page_title=".xls → .xlsx 변환기", layout="centered")
st.subheader("📂사이트매니저 .xls → .xlsx 변환")

def clean_cell(text):
    if isinstance(text, str):
        text = text.strip()
        if text.startswith("=\"") and text.endswith("\""):
            return text[2:-1]
        return text
    return text

uploaded_files = st.file_uploader("📂 사이트매니저 .xls 파일을 업로드하세요", type=["xls"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 변환 시작"):
        if len(uploaded_files) == 1:
            uploaded_file = uploaded_files[0]
            try:
                raw = uploaded_file.read()
                enc = chardet.detect(raw)['encoding'] or 'utf-8'
                html = raw.decode(enc, errors="ignore")

                soup = BeautifulSoup(html, "html.parser", from_encoding=enc)
                table = soup.find("table")
                rows = table.find_all("tr")
                data = []
                for row in rows:
                    cells = row.find_all(["td", "th"])
                    data.append([clean_cell(cell.get_text(strip=True)) for cell in cells])

                df = pd.DataFrame(data)
                df = pd.DataFrame(data)
                xlsx_io = BytesIO()
                new_name = uploaded_file.name.replace(".xls", ".xlsx")
                df.to_excel(xlsx_io, index=False, header=False, engine="openpyxl")
                st.download_button(
                    label="📥 변환된 .xlsx 다운로드",
                    data=xlsx_io.getvalue(),
                    file_name=new_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success(f"✅ 변환 완료: {uploaded_file.name} → {new_name}")
            except Exception as e:
                st.error(f"❌ 오류 발생: {uploaded_file.name}\n{e}")
        else:
            base_filename = datetime.today().strftime("%y%m%d")
            file_number = 0
            zip_filename = base_filename + ".zip"
            while os.path.exists(zip_filename):
                file_number += 1
                zip_filename = f"{base_filename}_{file_number}.zip"

            output_zip = BytesIO()
            with zipfile.ZipFile(output_zip, "w") as zf:
                for uploaded_file in uploaded_files:
                    try:
                        raw = uploaded_file.read()
                        try:
                            html = raw.decode("cp949")
                        except UnicodeDecodeError:
                            html = raw.decode("utf-8", errors="ignore")

                        soup = BeautifulSoup(html, "html.parser")
                        table = soup.find("table")
                        rows = table.find_all("tr")
                        data = []
                        for row in rows:
                            cells = row.find_all(["td", "th"])
                            data.append([clean_cell(cell.get_text(strip=True)) for cell in cells])

                        df = pd.DataFrame(data)
                        new_name = uploaded_file.name.replace(".xls", ".xlsx")
                        xlsx_io = BytesIO()
                        df.to_excel(xlsx_io, index=False, header=False, engine="openpyxl")
                        zf.writestr(new_name, xlsx_io.getvalue())
                        st.success(f"✅ 변환 완료: {uploaded_file.name} → {new_name}")
                    except Exception as e:
                        st.error(f"❌ 오류 발생: {uploaded_file.name}\n{e}")

            output_zip.seek(0)
            st.download_button(
                label="📦 변환된 .xlsx ZIP 다운로드",
                data=output_zip,
                file_name=zip_filename,
                mime="application/zip"
            )
