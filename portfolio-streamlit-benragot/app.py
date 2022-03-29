import streamlit as st
import app_resume
import app_crypto
import app_DFDC
import app_welcome
PAGES = {
    "Welcome": app_welcome,
    "Resume": app_resume,
    "DeepFake Detection Challenge": app_DFDC,
    "Ethereum mining interface": app_crypto,
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
