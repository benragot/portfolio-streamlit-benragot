'''
A module that displays the welcome page of the streamlit.
Its aim is only to display some information to explain the website.
'''

import streamlit as st
from PIL import Image
def app():
    st.title("Benjamin Ragot's Streamlit")
    st.markdown('### *A website that shows some of my skills.*')
    #showing my profile picture
    image = Image.open('images/app_resume/profile_picture.jpg')
    st.image(image, caption='A very nice picture of me at Le Wagon taken by the talented Benoit Billard.', use_column_width=True)
    st.markdown("""Welcome on my website! There are currently three sections that you can explore
                on the navigation bar on the left : \\
                :arrow_right: Resume : you will there find my resume in a pdf that you can easily download.\\
                :arrow_right: DeepFake Detection Challenge : you will there find a lot of information on the
                project I lead during the two last weeks of my formation of AI Developer.\\
                :arrow_right: Ethereum mining : you will there find out how I successfully built and optimized
                an infrastructure of three workers gathering 13 Graphics Processing Units.""")
