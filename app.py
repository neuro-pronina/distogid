import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from analysis import analyze_video
from reports import generate_pdf

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def check_password() -> bool:
    """Simple password authentication using STREAMLIT_PASSWORD."""
    def password_entered():
        if st.session_state.get("password") == os.getenv("STREAMLIT_PASSWORD"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct"):
        return True

    st.text_input("Пароль", type="password", on_change=password_entered, key="password")
    if st.session_state.get("password_correct") is False:
        st.error("Неверный пароль")
    return False


if not check_password():
    st.stop()

st.title("Distogid: анализ видео")

with st.form("upload-form"):
    patient_id = st.text_input("ID пациента")
    video_file = st.file_uploader("Видео (10–30 сек)", type=["mp4", "avi", "mov"])
    submitted = st.form_submit_button("Анализ")

if submitted:
    if not patient_id:
        st.error("Введите ID пациента")
    elif not video_file:
        st.error("Загрузите видеофайл")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = DATA_DIR / f"{patient_id}_{timestamp}.mp4"
        with open(video_path, "wb") as f:
            f.write(video_file.read())

        df = analyze_video(video_path)
        st.line_chart(df.set_index("time")[['yaw', 'pitch', 'roll']])

        json_bytes = df.to_json(orient="records").encode("utf-8")
        json_path = DATA_DIR / f"{patient_id}_{timestamp}.json"
        with open(json_path, "wb") as f:
            f.write(json_bytes)

        pdf_path = DATA_DIR / f"{patient_id}_{timestamp}.pdf"
        generate_pdf(patient_id, df, pdf_path)

        st.download_button("Скачать данные (JSON)", data=json_bytes,
                           file_name=json_path.name, mime="application/json")
        with open(pdf_path, "rb") as f:
            st.download_button("Скачать отчёт (PDF)", data=f.read(),
                               file_name=pdf_path.name, mime="application/pdf")
