import streamlit as st
import pandas as pd
import os
from pathlib import Path

# Import your existing functions
from Model_Connection_Code import model_response
from Preprocessing_Data_Code import preprocess
from Model_Connection_Code import generate_prompt_template
from Report_Generation_Code import generate_reports
from GTTS_Code import convert_to_speech, retry_single_tts

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "file_ready" not in st.session_state:
    st.session_state["file_ready"] = False

# Temp file path (declared outside for consistent access)
TEMP_FILE_PATH = "uploaded_student_reports.csv"

# Streamlit UI
st.title("📄 Student Report Generator")

uploaded_file = st.file_uploader("📂 Upload Student CSV File", type=["csv"])

if uploaded_file is not None:
    with open(TEMP_FILE_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ File uploaded successfully!")

    if st.button("📝 Generate Report"):
        st.session_state["page"] = "processing"
        st.session_state["file_ready"] = False

        df = generate_reports(TEMP_FILE_PATH)
        if isinstance(df, pd.DataFrame):
            df.to_csv(TEMP_FILE_PATH, index=False)
            st.session_state["file_ready"] = True
            st.success("✅ Reports generated!")
            if 'Generated_Report' in df.columns:
            	df['Generated_Report'] = df['Generated_Report'].astype(str)
            	try:
            		st.dataframe(df)
            	except Exception as e:
            		st.warning(f"Error rendering DataFrame: {e}")
            		st.table(df.astype(str))  # fallback

            #st.table(df)  # Show report after generation
        else:
            st.error(df)

if st.session_state.get("page") == "processing":
    st.header("⏳ Report Post-processing")
    with open(TEMP_FILE_PATH, "wb") as f:
        f.write(TEMP_FILE_PATH.getbuffer())

    if st.button("🔊 Convert to Speech"):
        # Read the updated CSV with the Generated_Report column
        message, status, result_df = convert_to_speech(TEMP_FILE_PATH)
        if status == 1:
            st.success(message)
            #st.dataframe(result_df)

            st.write("### ❗ Retry Failed Conversions")
            for idx, row in result_df[result_df["Speech_Status"].str.startswith("Failed")].iterrows():
                st.write(f"❌ Row {idx} - {row['Speech_Status']}")
                if st.button(f"🔁 Retry Speech for Row {idx}", key=f"retry_{idx}"):
                    retry_status = retry_single_tts(row["Generated_Report"], idx)
                    st.write(f"🔁 Retry Result for Row {idx}: {retry_status}")
        else:
            st.error(message)

    if st.session_state.get("file_ready"):
        st.success("🎉 All reports are ready for download!")
        with open(TEMP_FILE_PATH, "rb") as f:
            st.download_button("📥 Download Updated Report", f, file_name="updated_student_reports.csv", mime="text/csv")

