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
                - Christophe Morin ([LinkedIn](https://www.linkedin.com/in/christophe-morin-bb7b94a2/))\\
                Thanks a lot to them for their courage, their perseverance and their professionalism. Here is a picture
                of our team :muscle: :
                """)
    st.image("images/app_DFDC/DSC_7892.jpg", caption='A very nice picture of our team taken by Colin Chaigneau.')
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
    st.markdown("### The architecture we selected")
    st.markdown("""Our approach was based on a face classifier. This means that instead of analysing the whole video to
                tell if it is DeepFake or real, we will only select 10 images of it, as shown here :arrow_down:""")
    video = open('videos/aagfhgtpmv.mp4','rb')
    st.video(video)
    st.image("images/app_DFDC/sampling_images.png", caption='Sampling 10 images from the video')
    st.markdown("Then, for each image, we will select a face, thanks to a model called YoloV2 :")
    st.image("images/app_DFDC/sampling_faces.png", caption='Sampling one face per image')
    st.markdown("""Our Deep Learning model can then take the first face in input to output the probability that the face
                is fake. This Deep Learning model is based on a Convolutional Neural Network (CNN). They are perfect to
                analyse images.""")
    st.image("images/app_DFDC/simple_face_classifier.png", caption='The Deep Learning model')
    st.markdown("We can then reapeat this operation on the ten faces : ")
    st.image("images/app_DFDC/whole_face_classifier.png", caption='Computing the mean of the outputs of the Deep Learning model')
    st.markdown("Then, we can compare this mean to a threshold to finally indicate if the video is DeepFake or real :")
    st.image("images/app_DFDC/mean_threshold.png", caption='Comparing the mean to the threshold')
    st.markdown("""Here the threshold is 0.432... And you might wonder how we calculated it. Also, you might wonder how
                our Deep Learning model, the CNN, is able predict if a face is fake or real !\\
                Don't worry, we will discuss this in the next sections.""")

    st.markdown("### How we trained the Deep Learning model")
    st.markdown("""So, as we said earlier, the Deep Learning model must classify faces as DeepFake (=1) or real (=0).
                To do so, we must train it on a dataset. We first choose a simple dataset of 32 000 faces with an equal
                quantity of fake and real faces. Faces are easier to process since they are small images. Here, we
                choose to resize them as 224x224 pixels images. It was a good way to find out which CNN architecture
                could give us interesting results. Below, a small gif that shows some faces from the dataset we used.
                You should easily find out which ones are fake ! :arrow_down:""")
    st.image("images/app_DFDC/faces.gif", caption='A few faces from the small dataset')
    st.markdown("""With this dataset, we found out that the best CNN architecture we found was based on three
                convolutional layers, with 16, 32 and 64 filters. We also learned a lot about how to deal with the
                training a Deep Learning model on a big dataset, with batch per batch training.""")
    st.markdown("""This method gave us results that were encouraging by beating the baseline. We reached 60\%
                accuracy quite easily and we were ready to go to the next step : creating a bigger dataset.""")
    st.markdown("""As mentioned earlier, we were given 120 000 videos in the original dataset. Around 19 000 videos
                were real, so we kept them and selected another 19 000 videos among the DeepFake ones to have a balanced
                dataset.""")
    st.markdown("""Each video lasts 10 seconds, with 30 images per second : there is therefore 300 images for each
                video. Moreover, each image was 1920x1080 pixels. Our aim was to reduce this quantity of information to
                train smartly our CNN. \\
                1. First, we took one image out of three : we now only have 100 images per video.\\
                2. Then, we selected one face per image, reducing the size of the image to process to 224x224 pixels. We
                now have 100 faces per video. \\
                3. """)
    st.markdown("### How we selected our CNN architecture")

    #sharing the folder of the best classifier of faces
