import streamlit as st
from PIL import Image
def app():
    st.markdown('# :construction_worker: Currently being developed ! :construction_worker:')
    st.title("Benjamin Ragot's Streamlit")
    st.markdown('## Welcome on my streamlit !')
    st.markdown('### This is a website that shows some of my skills as a Junior Data Scientist.')
    #showing my profile picture
    image = Image.open('images/app_resume/profile_picture.jpg')
    st.image(image, caption='A very nice picture of me at Le Wagon taken by the talented Benoit Billard.', use_column_width=True)
