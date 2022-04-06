'''
A module that displays the DeepFake Detection Challenge of the Streamlit. It tells the story
of how we built a model that can classify videos as DeepFake or Real.
'''

import streamlit as st
def app():
    st.title("DeepFake Detection Challenge")
    st.markdown('An article to show how we dealt with the famous kaggle dataset to develop a video classifier.')
    if st.checkbox('You do not feel like reading ? Tick the box to watch a short video (7min) that sums up our work !'):
        st.video("https://youtu.be/vwwDGtuFbSQ?t=748",start_time=750)

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
                - Christophe Morin ([Lindatasetay its quality is almost like the one you could get in a movie.
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
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.image("images/app_DFDC/faces.gif", caption='A few faces from the small dataset')
    with col3:
        st.write("")

    st.markdown("""With this dataset, we found out that the best CNN architecture on three
                convolutional layers, with 16, 32 and 64 filters. We also learned a lot about how to deal with the
                training a Deep Learning model on a big dataset, with batch per batch training.""")
    st.markdown("""This method gave us results that were encouraging by beating the baseline. We reached 60\%
                accuracy quite easily and we were ready to go to the next step : creating a bigger dataset.""")
    st.markdown("""As mentioned earlier, we were given 120 000 videos in the original dataset. Around 19 000 videos
                were real, so we kept them and selected another 19 000 videos among the DeepFake ones to have a balanced
                dataset.""")

    st.markdown("""Each video lasts 10 seconds, with 30 images per second : there is therefore 300 images for each
                video. Moreover, each image was 1920x1080 pixels. Our aim was to reduce this quantity of information to
                train smartly our CNN.\\
                1. First, we took one image out of three : we now only have 100 images per video.\\
                2. Then, we selected one face per image, reducing the size of the image to process to 224x224 pixels. We
                now have 100 faces per video. \\
                3. Having 38 000 videos, we are now dealing with 3 800 000 faces ! It is way too much, we needed to stay
                around 100 000 faces. We did so by picking only three faces per video. But if we pick randomly three
                faces, we might have images that ar quite the same, especially on videos where the people do not move
                much : """)
    st.image('images/app_DFDC/random_faces.png')

    st.markdown("""4. To get three faces that as much different one from another, we then calculated the difference
                between each face. Thanks to this method, we can then select three interesting faces : """)
    st.image('images/app_DFDC/selected_faces.png')
    st.markdown("""Tanks to this method, we gathered 114 000 faces. We then used them to train an fine-tune a Deep
                Learning model ! """)

    st.markdown("### How we selected our CNN architecture")
    st.markdown("""We basically already had a good architecture of CNN based on three convolutional layers, with 16, 32
                and 64 filters. We did not have much time in front of us, and limited computing power : we were using
                Google Colab. For each model we trained, we saved information in a Google Drive that you can view
                [here](https://drive.google.com/drive/folders/1hbekEzHPAHqhgndpn-hC0HTaBizMHyUh?usp=sharing). Finally,
                we were able to get really good results thanks to this architecture :""")
    st.image('images/app_DFDC/best_model.png', use_column_width=True, caption='A scheme of the model used to classify faces')
    st.markdown("""Our results were quite good on this one : 75\% accuracy and almost 80\% of recall !""")
    if st.checkbox('You feel like knowing more on this model ? Click me to have a some more information !'):
        st.markdown("""Here is a link to the folder where we stored all the information about this model :
                    [Our best model](https://drive.google.com/file/d/11jP8aL0RA2QfqvxdaQJO98f9bdjmoNTn/view?usp=sharing)\\
                    You can browse it freely, but you might enjoy more our analysis which is right below.""")
        if st.checkbox('Click me to show the summary of our model '):
            st.image('images/app_DFDC/model_summary.png', caption='Our model\'s summary')
        st.markdown("""As you can see, there are a few keypoints that really helped us fine-tune our model : \\
                    1. Using the 16, 32 and 64 filters of convolutional layers. We tried to replicate an architecture
                    from  [this article](https://www.sciencedirect.com/science/article/pii/S2667096821000471).\\
                    2. Choosing wisely the kernel sizes for our convolutionnal layers. Here, the shape used was (3,3).\\
                    3. Choosing wisely max pool size. Here, we chose (4,4).\\
                    4. Choosing wisely our dense layers. Here, the best we found were a layer of 128 neurons, then a
                    layer of 16 neurons and of course an output layer of one neuron.\\
                    5. Selecting the right dropout rate to avoid overfitting, which could be a risk because we took
                    three faces per video. Here, we chose 0.1.
                    """)
        st.markdown("""In the end, our best leverage to increase our scores was still to get more faces to train on,
                    even though this fine tuning allowed us to extract the last percents of accuracy, recall and
                    precision we could get.
                    """)
    st.markdown("## What we learned")
    st.markdown("### Our successes")
    st.markdown("""Well, we could not have worked and learned more in two weeks. Here's a short list of all the
                technologies/methods we used :\\
                - Google Cloud Platform (GCP) : we used virtual machines to download and unzip the 500 GB dataset in a
                bucket. Then we mostly used Vertex AI workbench to share a JupyterLab on a machine with a correct
                computing power.\\
                - TensorFlow/Keras : we used it to create and train our Deep Learning model.\\
                - YoloV2 : we used it to find faces on images\\
                - Github : we learned to work as a team, establishing inputs/outputs of our modules/functions to
                keeep the workflow smooth.\\
                - Trello : we used this organization tool to assign us tasks and observe our progress while working on
                this challenging project.\\
                - We achieved our goal : we have a function that can process a video and predict if it's a DeepFake or not !\\
                - Bonus : we created a function that transforms a video into a gif where we plot the probability that
                the face is fake with a bounding box : """)
    st.image('images/app_DFDC/dumb.gif')
    st.markdown("### Our failures")
    st.markdown("""Part of learning is making mistakes, and there is always room for improvement. It would be nonsense
                to pretend everything went without a problem ! Here's a shortlist of our most epic fails : \\
                - Trying to get some GPU computing power with free GCP (Google Cloud Platform) credits : impossible. With
                the context of GPU shortage, GCP is only allowing people with real credits and loyal customers. We tried
                to train models on my laptop but it was not very fast. We finally used Google Colab Pro which is quite
                cheap (12$/month). But we should have done it at the very beginning ! \\
                - Failing to use Google Colab properly due to different geographical locations. We've had troubles with
                the loading of the images from my Google Drive to Google Colab. It's quite simple : Google Colab
                computing power is in the U.S. an my Drive is in Europe. So loading images one by one without zipping
                anything lead us to think that we could not use Google Colab !\\
                - Trying to show which image maximizes a filter from convolutional layers : unfortunately since our model
                can classify fake and real faces based on details the results was not something very clear to a human's
                eye.\\
                - Trying to make sure every face is perfectly vertically aligned : it was a good idea that could have
                lead us to better results but unfortunately, we were using 224/224 pixels images that were not always
                well recognized by the model used to align face so it was not very successful and took a lot of computing
                time. More information [here](https://datahacker.rs/010-how-to-align-faces-with-opencv-in-python/).""")

    st.markdown("""On a more personal note :\\
                As mentioned before, this challenge was supposed to be done in four months
                and we only had two weeks. Therefore, it was really hard for me, the team leader, to not being able to
                support my teammates when they wanted to explore different model architecture with eye blinking or face
                contours analysis for instance. We were in a very tight schedule and at the beginning I hoped we would
                have the time for some exploration but unfortunately we did not !
                """)

    st.markdown("# Conclusion")
    st.markdown("""To put in a nutshell, this challenge was one of the richest experience I have ever participated.
                It was really hard, but we overcame the difficulties one by one to produce something in only two
                weeks, which I am really proud of. Moreover, it was such a pleasure to work with Jean-Baptiste,
                Christophe and Ulysse : they were really motivated by the project and they showed a very
                appreciated autonomy in their work. This concluded the end of my bootcamp at Le Wagon and let's be
                honest : it could not have ended in a better way.""")
