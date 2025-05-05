import streamlit as st
import random
import smtplib
from email.message import EmailMessage
from utils import load_css, centered_form
from db import add_user, email_exists
import regex as re

EMAIL_ADDRESS = "mocharlavarsha@gmail.com"
EMAIL_PASSWORD = "azvf eqhu fngm twoq"  # ideally use st.secrets

def send_otp(email, otp):
    msg = EmailMessage()
    msg.set_content(f"Your OTP for verification is: {otp}")
    msg["Subject"] = "OTP Verification"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send OTP: {e}")
        return False

def show_signup(switch_page):
    # load_css("styles/base.css")
    load_css("styles/signup.css")
    if "otp_stage" not in st.session_state:
        st.session_state.otp_stage = False

    def show_form():
        st.markdown("<h1 class='text-center'>🔐 Sign Up</h1>", unsafe_allow_html=True)

        # Real-time password input
        with st.form("signup_form"):
            name = st.text_input("Full Name", placeholder="e.g., Chintam Gopi ")
            email = st.text_input("Email", placeholder="e.g., gopi123@gmail.com")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
            st.caption("Password length must be at least 8 characters, with lowercase, uppercase, and a special character.")

            # Password strength check
            def check_password_strength(pw):
                strength = 0
                if len(pw) >= 8:
                    strength += 1
                if re.search(r'[a-z]', pw):
                    strength += 1
                if re.search(r'[A-Z]', pw):
                    strength += 1
                if re.search(r'\d', pw):
                    strength += 1
                if re.search(r'[!@#$%^&*(),.?":{}|<>]', pw):
                    strength += 1
                return strength

            if password:
                strength = check_password_strength(password)
                if strength <= 2:
                    st.warning("🔴 Weak password. Try adding uppercase letters, numbers, or symbols.")
                elif strength in [3, 4]:
                    st.info("🟡 Moderate password. Almost there!")
                elif strength == 5:
                    st.success("🟢 Strong password!")

            confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm password")
            if confirm_password:
                if confirm_password!=password:
                    st.error("Passwords does not match")
                else:
                    st.success("Passwords are matched")
            agree = st.checkbox("I agree to the Terms and Conditions")
            submitted = st.form_submit_button("Create Account")
            if submitted:
                if not (name and email and password and confirm_password):
                    st.warning("❗ All fields are required.")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match.")
                elif len(password) < 8 or not re.search(r'[a-z]', password) \
                        or not re.search(r'[A-Z]', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                    st.error("🔐 Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one special character.") 
                elif not agree:
                    st.warning("☑️ Please agree to the Terms and Conditions.")
                elif email_exists(email):
                    st.warning("⚠️ User with this email already exists.")
                else:
                    otp = str(random.randint(100000, 999999))
                    if send_otp(email, otp):
                        st.session_state.otp = otp
                        st.session_state.pending_user = {
                            "name": name,
                            "email": email,
                            "password": password
                        }
                        st.session_state.otp_stage = True
                        st.success("✅ OTP sent to your email.")
                    else:
                        st.error("Failed to send OTP. Please try again later.")
            st.markdown("<div style='text-align:left;'>Already have an account? </div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.form_submit_button("👩‍💼 Login", use_container_width=True, on_click=lambda: switch_page("login"))
            with col2:
                st.form_submit_button("🏠 Back to Home", use_container_width=True, on_click=lambda: switch_page("home"))

    def show_otp_verification():
        st.markdown("<h2 class='text-center'>📨 Verify OTP</h2>", unsafe_allow_html=True)
        st.info("Check your email and enter the OTP below.")

        otp_input = st.text_input("Enter OTP", max_chars=6)
        if st.button("Verify OTP"):
            if otp_input == st.session_state.otp:
                user = st.session_state.pending_user
                if add_user(user["name"], user["email"], user["password"]):
                    st.success("✅ Account created successfully!")
                    # Clean up
                    del st.session_state.otp_stage
                    del st.session_state.otp
                    del st.session_state.pending_user
                    switch_page("login")
                else:
                    st.error("Failed to create user. Try again.")
            else:
                st.error("❌ Incorrect OTP. Please try again.")

        if st.button("Resend OTP"):
            otp = str(random.randint(100000, 999999))
            st.session_state.otp = otp
            send_otp(st.session_state.pending_user["email"], otp)
            st.success("📨 New OTP sent.")

    if not st.session_state.otp_stage:
        centered_form(show_form)
    else:
        centered_form(show_otp_verification)