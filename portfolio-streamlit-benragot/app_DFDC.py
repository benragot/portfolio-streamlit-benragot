import streamlit as st
import io
def app():
    st.markdown('# :construction_worker: Currently being developed ! :construction_worker:')
    st.title("DeepFake Detection Challenge")
    st.markdown('A nice interface to show how we dealt with the famous kaggle dataset to develop a video classifier.')
    if st.checkbox('You do not feel like reading ? Tick the box to see a short video (7min) that sums up our work !'):
        st.video("https://youtu.be/vwwDGtuFbSQ?t=748")

    st.markdown("## Context")
    st.markdown("""After weeks of studying at [Le Wagon](https://www.lewagon.com/paris/data-science-course/full-time),
                we were about to begin what we were all waiting for : the projects. In fact, I was quite involved
                because I decided to propose a real challenge : creating a DeepFake video classifier based on the
                [Kaggle competition](https://www.kaggle.com/c/deepfake-detection-challenge) that happened two years ago.\\
                Therefore, I pitched this project in front of all the other students without forgetting to tell them
                that we will have to do in two weeks what the competitors did in four months !\\
                Then, three people were brave enough to join me on this crazy and challenging adventure :\\
                - Jean-Baptiste Bordenave ([LinkedIn](https://www.linkedin.com/in/jean-baptiste-bordenave-b488b1116/))\\
                - Ulysse Gatard ([LinkedIn](https://www.linkedin.com/in/ulysse-gatard-976b9967/))\\
                - Christophe Morin ([LinkedIn](https://www.linkedin.com/in/christophe-morin-bb7b94a2/))
                Thanks a lot to them for their courage, their perseverance and their professionalism.
                """)

    st.markdown("## What is a DeepFake ?")
    st.markdown("A DeepFake is a __*falsified video*__.")
    st.markdown("""Here is a very good definition from  OxfordLanguages : *\"a video of a person in which their face or
                body has been digitally altered so that they appear to be someone else, typically used maliciously or to
                spread false information.\"*""")
    st.markdown("Let's see an example with Barack Obama :")
    st.video('https://www.youtube.com/watch?v=cQ54GDm1eL0')
    st.markdown("""Even though it really looks like it is Obama speaking __it is not__! In fact, this DeepFake is really
                well done : we could say its quality is almost like the one you could get in a movie.
                Therefore, this kind of DeepFake is quite long and expensive to create.""")


    st.markdown("## The DeepFake Detection Challenge (DFDC)")
    st.markdown(""" The DeepFake Detection Challenge is a competition that took place two years ago. Given a dataset
                of 120 000 videos of 10 seconds each, the teams had to build a model that could tell if a video was
                DeepFake or Real. You can find more information here :
                [Kaggle DFDC](https://www.kaggle.com/c/deepfake-detection-challenge).
                """)
    st.markdown(""" The dataset given in this challenge was based on homemade videos : the quality of the DeepFakes
                was quite heterogeneous. They were homemade because the aim of the competition was to detect DeepFakes
                among videos that you can find on social networks for instance : we can assume that most of them will
                not be as good as Obama's !
                """)
    st.markdown('This one :arrow_down: is quite bad : the mask applied on the head of the man is flickering :')
    # showing a bad deepfake
    video = open('videos/aagfhgtpmv.mp4','rb')
    st.video(video)
    st.markdown('This one :arrow_down: is much better : the mask fits almost perfectly the woman !')
    # showing a good deepfake
    video = open('videos/acxnxvbsxk.mp4','rb')
    st.video(video)
    # making the reader guess
    # showing a good deepfake
    st.markdown("Now that you know more on this technology, can you guess if this one :arrow_down: is DeepFake or Real ?")
    video = open('videos/btmsngnqhv.mp4','rb')
    st.video(video)
    if st.button('It\'s Real !'):
        st.error("""False ! It was DeepFake. You know get how hard it is to guess, especially when the person is a
                 little bit far away !""")
    if st.button('It\'s fake !'):
        st.success("""True ! It was DeepFake. You are indeed quite good at classifying videos ! But you might get now how
                 hard it will be to make a model as good as you !""")


    st.markdown("## Our approach")
    st.markdown(" Our approach")
