'''import streamlit as st
from db import create_table
from pages.home import show_home
from pages.signup import show_signup
from pages.admin import show_admin_panel
from pages.login import show_login
from pages.dashboard import show_dashboard 
from utils import load_css, centered_form

#page setup
st.set_page_config(page_title="User Management App", layout="centered", initial_sidebar_state="collapsed")
#load css file
load_css("styles/main.css")
create_table()

# Hide sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# Session state for page switching
if "page" not in st.session_state:
    st.session_state.page = "home"

def switch_page(page_name):
    st.session_state.page = page_name

# Run the correct page
if st.session_state.page == "home":
    show_home(switch_page)
elif st.session_state.page == "signup":
    show_signup(switch_page)
elif st.session_state.page == "admin":
    show_admin_panel(switch_page)
elif st.session_state.page =="login":
    show_login(switch_page)
elif st.session_state.page =="dashboard":
    show_dashboard(switch_page)'''
import streamlit as st
from db import create_table
from pages.home import show_home
from pages.signup import show_signup
from pages.admin import show_admin_panel
from pages.login import show_login
from pages.dashboard import show_dashboard 
from utils import load_css, centered_form

# Page setup
st.set_page_config(page_title="Progress Report Generation App", layout="centered", initial_sidebar_state="collapsed")

# Hide sidebar immediately
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# Session state for page switching
if "page" not in st.session_state:
    st.session_state.page = "home"

def switch_page(page_name):
    st.session_state.page = page_name

# 📦 Move database and CSS loading here (after session setup)
def main():
    load_css("styles/main.css")
    create_table()

    # Run the correct page
    if st.session_state.page == "home":
        show_home(switch_page)
    elif st.session_state.page == "signup":
        show_signup(switch_page)
    elif st.session_state.page == "admin":
        show_admin_panel(switch_page)
    elif st.session_state.page == "login":
        show_login(switch_page)
    elif st.session_state.page == "dashboard":
        show_dashboard(switch_page)

if __name__ == "__main__":
    main()


