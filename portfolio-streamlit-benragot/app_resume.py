'''
A module that displays the resume's page. Right now there is only two resumes, one in French
and one in English.
#todo : One improvement could be to update the page with a real resume of the journey that lead
me to become a Data Scientist.
'''

import streamlit as st
import base64
def app():
    st.title("Benjamin Ragot's Resume")
    st.markdown("### Here is my resume. Please feel free to download it.")
    language = st.radio(f'Select a language', ('English', 'Français'))
    if language == 'English':
        with open('images/app_resume/CV_en.1.0.pdf', 'rb') as f:
            st.download_button('Download', f, file_name='CV_Benjamin_Ragot.pdf')
        st.image('images/app_resume/CV_en.1.0.png')
    else:
        with open('images/app_resume/CV.0.9.pdf', 'rb') as f:
            st.download_button('Download', f, file_name='CV_Benjamin_Ragot.pdf')
        st.image('images/app_resume/CV.0.9.png')
