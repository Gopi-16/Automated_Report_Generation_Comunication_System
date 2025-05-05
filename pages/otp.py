import streamlit as st
from db import add_user
from utils import load_css, centered_form

def show_otp(switch_page):
    load_css("styles/base.css")

    def otp_form():
        st.markdown("<h2 class='text-center'>🔐 Verify OTP</h2>", unsafe_allow_html=True)

        if "otp" not in st.session_state or "pending_user" not in st.session_state:
            st.warning("No OTP pending. Please sign up first.")
            if st.button("🔙 Go to Signup"):
                switch_page("signup")
            return

        with st.form("verify_otp_form"):
            user_otp = st.text_input("Enter the OTP sent to your email", max_chars=6)

            if st.form_submit_button("Verify"):
                if user_otp == st.session_state.otp:
                    data = st.session_state.pending_user
                    if add_user(data["name"], data["email"], data["password"]):
                        st.success("✅ Account created successfully!")
                        st.session_state.pop("otp")
                        st.session_state.pop("pending_user")
                        switch_page("login")
                    else:
                        st.error("❌ Failed to create account. Try again.")
                else:
                    st.error("❌ Invalid OTP. Please try again.")

        if st.button("Resend OTP"):
            import random
            from signup import send_otp  # ensure this works if send_otp is moved to shared module
            otp = str(random.randint(100000, 999999))
            st.session_state.otp = otp
            send_otp(st.session_state.pending_user["email"], otp)
            st.success("📨 OTP resent to your email.")

    centered_form(otp_form)
