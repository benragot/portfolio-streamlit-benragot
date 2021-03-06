'''
Main module of the Streamlit. It is only in charge of displaying one of the pages registered
in the PAGES dictionary.
'''

import streamlit as st
import app_resume
import app_crypto
import app_DFDC
import app_LDA_demo
import app_welcome
PAGES = {
    "Welcome": app_welcome,
    "Resume": app_resume,
    "DeepFake Detection Challenge": app_DFDC,
    "NLP : LDA demo": app_LDA_demo,
    "Ethereum mining": app_crypto,
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
