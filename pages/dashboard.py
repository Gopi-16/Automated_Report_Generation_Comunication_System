import streamlit as st
import pandas as pd
import os
import tempfile
import shutil
import concurrent.futures
import time

# Local module imports
from utils import load_css
from Model_Connection_Code import model_response, generate_prompt_template
from Preprocessing_Data_Code import preprocess
from Refining_Response_Code import refine_response
from Report_Generation_Code import generate_reports
from GTTS_Code import convert_speech
from mail import run_mailing
from Chat_Bot.Vector_Data_Store_Embed import create_index_file
from Chat_Bot.Model_Connection_Rag import question
from tele_gram_bot import send_reports
import asyncio
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

# File names
uploaded_temp = "uploaded_dat.csv"
processed_temp = "processed_reports.csv"

# Session State Initialization
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "bg_status" not in st.session_state:
    st.session_state.bg_status = None
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "file_ready" not in st.session_state:
    st.session_state.file_ready = False
if "audio_ready" not in st.session_state:
    st.session_state.audio_ready = False
if "speech_failures" not in st.session_state:
    st.session_state.speech_failures = []
if "temp_audio_folder" not in st.session_state:
    st.session_state.temp_audio_folder = None
if "_temp_audio_dir_obj" not in st.session_state:
    st.session_state._temp_audio_dir_obj = None
if "reports_df" not in st.session_state:
    st.session_state.reports_df = None
if "run_report" not in st.session_state:
    st.session_state.run_report = False
if "run_audio" not in st.session_state:
    st.session_state.run_audio = False
if "run_audio_failed" not in st.session_state:
    st.session_state.run_audio_failed = False
if "run_mail" not in st.session_state:
    st.session_state.run_mail = False
if "report_downloaded" not in st.session_state:
    st.session_state.report_downloaded = False


# Background Tasks
def run_report_pipeline_bg():
    if os.path.exists(uploaded_temp):
        df = generate_reports(uploaded_temp)
        if "Generated_Report" in df.columns:
            df["Generated_Report"] = df["Generated_Report"].astype(str)
            df["Status"] = df["Status"].map({1: "Success", 0: "Fail"})
            df.to_csv(processed_temp, index=False)
            shutil.copyfile(processed_temp, uploaded_temp)
            st.session_state.reports_df = df
            st.session_state.file_ready = True
            st.session_state.report_generated = (df["Status"] == "Fail").any()
            st.session_state.bg_status = "✅ Reports generated!"
        else:
            st.session_state.bg_status = "⚠️ Report generation failed (invalid DataFrame)."
    else:
        st.session_state.bg_status = "⚠️ Uploaded file not found."

def run_audio_conversion_bg(failed_only=False):
    audio_folder = st.session_state.temp_audio_folder
    reports = st.session_state.reports_df["Generated_Report"].tolist()
    if failed_only:
        failed_indexes = st.session_state.get("speech_failures", [])
        reports = [reports[i] for i in failed_indexes]
    result = convert_speech(reports, audio_folder)
    
    st.session_state.audio_ready = True
    st.session_state.speech_failures = result.get("failed", [])
    st.session_state.bg_status = "🎤 Audio conversion complete."

def run_mailing_thread_bg():
    if os.path.exists(processed_temp):
        audio_folder = st.session_state.temp_audio_folder
        reports = st.session_state.reports_df["Generated_Report"].tolist()
        sent, failed = run_mailing(processed_temp, st.session_state.temp_audio_folder)
        
        if failed:
            st.session_state.bg_status = f"✅ Sent to {len(sent)} emails. ⚠️ Failed: {len(failed)}"
        else:
            st.session_state.bg_status = f"✅ All emails sent!"
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(send_reports(st.session_state.reports_df, audio_folder))
            st.session_state.bg_status = "✅ Reports sent via Telegram!"
        except Exception as e:
            st.session_state.bg_status = f"❌ Telegram sending failed: {e}"
        finally:
            loop.close()
   

    else:
        st.session_state.bg_status = "❌ Processed report file not found."

def run_chatbot_response(user_input):
    return question(user_input)

# Main Dashboard
def show_dashboard(switch_page):
    load_css("styles/base.css")
    load_css("styles/dashboard.css")
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="dashboard-title">🎉 Welcome!</h1>', unsafe_allow_html=True)
    st.markdown('<p class="dashboard-subtext">You have successfully signed in.</p>', unsafe_allow_html=True)

    # UI Buttons
    col1, col2, col3, col4, col5 = st.columns([3, 3, 3, 3, 3])
    with col1:
        button_label = "📝 Generate Report" if not st.session_state.report_generated else "🔁 Regenerate Failed Reports"
        if st.button(button_label):
            st.session_state.run_report = True

    with col2:
        if st.session_state.file_ready:
            if st.button("🔊 Convert to Speech"):
                st.session_state.run_audio = True

    with col3:
        if st.session_state.speech_failures:
            if st.button("🔁 Regenerate Failed Audio"):
                st.session_state.run_audio_failed = True

    with col4:
        if st.session_state.audio_ready:
            if st.button("📬 Send Mails"):
                st.session_state.run_mail = True

    with col5:
        if st.button("🚪 Logout"):
            st.session_state.clear()
            switch_page("home")

    left_col, right_col = st.columns([7, 5])
    # File Upload
    with left_col:
        uploaded_file = st.file_uploader("📤 Upload CSV File for Mailing", type=["csv"])
        if uploaded_file and not st.session_state.file_uploaded:
            with open(uploaded_temp, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.file_uploaded = True
            st.session_state.file_ready = False
            st.success("✅ File uploaded successfully.")

        # Setup audio folder
        if not st.session_state.temp_audio_folder:
            temp_dir = tempfile.TemporaryDirectory()
            st.session_state.temp_audio_folder = temp_dir.name
            st.session_state._temp_audio_dir_obj = temp_dir

        # Background processes
        if st.session_state.run_report:
            with st.spinner("Generating Reports..."):
                run_report_pipeline_bg()
            st.session_state.run_report = False

        if st.session_state.run_audio:
            with st.spinner("Converting to Audio..."):
                run_audio_conversion_bg(failed_only=False)
            st.session_state.run_audio = False

        if st.session_state.run_audio_failed:
            with st.spinner("Regenerating Failed Audio..."):
                run_audio_conversion_bg(failed_only=True)
            st.session_state.run_audio_failed = False

        if st.session_state.run_mail:
            with st.spinner("Sending Emails..."):
                run_mailing_thread_bg()
            st.session_state.run_mail = False

        # Status Message
        if st.session_state.bg_status:
            st.info(st.session_state.bg_status)

        # Downloads
        if st.session_state.file_ready:
            
            st.markdown("### 📋 Generated Student Reports")
            st.dataframe(
            st.session_state.reports_df[["Name", "gmail", "Status"]],
            use_container_width=True)
            st.session_state.report_downloaded = True

            with open(processed_temp, "rb") as f:
                if st.download_button("⬇️ Download Reports CSV", f, file_name="student_reports.csv"):
                    st.session_state.report_downloaded = True

        if st.session_state.audio_ready:
            for audio_file in os.listdir(st.session_state.temp_audio_folder):
                file_path = os.path.join(st.session_state.temp_audio_folder, audio_file)
                with open(file_path, "rb") as f:
                    st.download_button(f"⬇️ {audio_file}", f, file_name=audio_file)
    with right_col:
    # Chatbot
        
        st.markdown("#### 🤖 Chat with Assistant")
        user_input = st.chat_input("Ask something...")
        if user_input:
            with st.spinner("Thinking..."):
                response = run_chatbot_response(user_input)
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("bot", response))
        for sender, msg in st.session_state.chat_history[-6:]:
            if sender == "user":
                st.chat_message("user").write(msg)
            else:
                st.chat_message("assistant").write(msg)

    st.markdown("</div>", unsafe_allow_html=True)
