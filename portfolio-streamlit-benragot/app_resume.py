import streamlit as st
from PIL import Image
import base64
def app():
    st.markdown('# :construction_worker: Currently being developed ! :construction_worker:')
    st.title("Benjamin Ragot's Resume")
    st.markdown('### A nice interface to show who I am.')
    if st.checkbox('Show me directly your resume !'):
        with open('images/app_resume/CV.0.9.pdf',"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    st.markdown('## So, Who am I then?')
    #showing my profile picture
    image = Image.open('images/app_resume/profile_picture.jpg')
    st.image(image, caption='A very nice picture of me at Le Wagon taken by the talented Benoit Billard.')
    st.markdown('- Benjamin Ragot')
    st.markdown('- :birthday: 26 years old')
    st.markdown('- :round_pushpin: Paris :fr:')
    st.markdown('- :envelope: br.ragot@gmail.com')
