import streamlit as st
import os

def load_css(file_path):
    st.markdown("""
    <style>
    input {
        autocomplete: new-password !important;
    }
    </style>
""", unsafe_allow_html=True)

    abs_path = os.path.abspath(file_path)
    try:
        with open(abs_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found at: {abs_path}")

def centered_form(content_fn):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)  # ✅ starts styled container
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        content_fn()

    st.markdown("</div>", unsafe_allow_html=True)  # ✅ close styled containe

def with_main_container(content_fn):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("<!-- inside with_main_container -->", unsafe_allow_html=True)
    content_fn()
    st.markdown('</div>', unsafe_allow_html=True)
