import streamlit as st
from utils import centered_form, load_css
from db import verify_user

def show_login(switch_page):
    load_css("styles/login.css")

    # Inject autofill prevention
    st.markdown("""
        <input type="text" name="fakeuser" autocomplete="username" style="display:none">
        <input type="password" name="fakepass" autocomplete="new-password" style="display:none">
        <script>
        const forms = window.parent.document.querySelectorAll("form");
        forms.forEach(form => {
            form.setAttribute("autocomplete", "off");
            const inputs = form.querySelectorAll("input");
            inputs.forEach(input => {
                input.setAttribute("autocomplete", "off");
                input.setAttribute("readonly", true);
                setTimeout(() => input.removeAttribute("readonly"), 500);
            });
        });
        </script>
        <style>
            input:-webkit-autofill {
                box-shadow: 0 0 0 1000px white inset !important;
                -webkit-text-fill-color: black !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # UI inside a function for centered_form
    def form_ui():
        st.markdown("<h1>👤 Secure Login</h1>", unsafe_allow_html=True)

        username = st.text_input("Email 🧑‍💻", placeholder="Enter email", key="u_field")
        secret = st.text_input("Password 🔒", type="password", placeholder="Enter passcode", key="s_field")

        col1, col2 = st.columns(2)

        login_clicked = col1.button("Login")
        back_clicked = col2.button("Back to Home")

        if login_clicked:
            if verify_user(username, secret):
                st.success("Welcome!")
                st.session_state['authenticated'] = True
                switch_page("dashboard")
            else:
                st.error("❌ Wrong credentials")

        elif back_clicked:
            switch_page("home")

    centered_form(form_ui)
