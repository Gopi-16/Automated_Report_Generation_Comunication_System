import streamlit as st

from utils import with_main_container


def show_home(switch_page):
    def content():
        st.title("🏠 Welcome to the User Management App")
        st.markdown("Manage users with encrypted passwords and a secure admin panel for full control.")
        st.markdown("---")
        st.markdown("### 🚀 Get Started")
        st.markdown("Choose an option below to begin:")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("🔐 Sign Up", use_container_width=True, on_click=lambda: switch_page("signup"))
        with col2:
            st.button("👩‍💼 Login", use_container_width=True, on_click=lambda: switch_page("login"))
        with col3:
            st.button("🛠️ Admin Panel", use_container_width=True, on_click=lambda: switch_page("admin"))

    with_main_container(content)
