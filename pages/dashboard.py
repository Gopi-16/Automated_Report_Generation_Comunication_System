default_values = {
    "report_generated": False,
    "chat_history": [],
    "bg_status": None,
    "file_uploaded": False,
    "file_ready": False,
    "audio_ready": False,
    "speech_failures": [],
    "temp_audio_folder": None,
    "_temp_audio_dir_obj": None,
    "reports_df": None,
    "run_report": False,
    "run_audio": False,
    "run_audio_failed": False,
    "run_mail": False,
    "report_downloaded": False,
}

for key, default in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = default
