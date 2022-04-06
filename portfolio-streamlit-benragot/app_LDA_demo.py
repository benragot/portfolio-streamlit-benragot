'''
A module that displays the LDA demo's page.
https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation
'''

import streamlit as st
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import download as nltkDL
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from deep_translator import GoogleTranslator

#functions to manipulate text before analysing it
def remove_punctuation(txt):
    for punctuation in string.punctuation:
        txt = txt.replace(punctuation, '')
    return txt
def lower_txt(txt):
    return txt.lower()
def remove_numbers(txt):
    return ''.join(word for word in txt if not word.isdigit())
def remove_stopwords(txt):
    stop_words = set(stopwords.words('portuguese'))
    word_tokens = word_tokenize(txt)
    txt = [w for w in word_tokens if not w in stop_words]
    return txt
def lemmatize(txt_list):
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word) for word in txt_list]
    return ' '.join(lemmatized)

def compute_and_show_LDA_results(data,n_components,nb_words,translate,language):
    latest_iteration = st.empty()
    bar = st.progress(0)
    results = {}
    latest_iteration.text(f'Vectorizer fitting...')
    vectorizer = TfidfVectorizer().fit(data)
    bar.progress(10)
    latest_iteration.text(f'Vectorizing data...')
    data_vectorized = vectorizer.transform(data)
    bar.progress(20)
    latest_iteration.text(f'Fitting the LDA model...')
    lda_model = LatentDirichletAllocation(n_components=n_components,n_jobs=-1).fit(data_vectorized)
    bar.progress(30)
    for idx, topic in enumerate(lda_model.components_):
        if translate:
            latest_iteration.text(f'Translating results...  Topic {idx + 1}/{n_components}')
            results[f"Topic {idx + 1}"] = [(GoogleTranslator(source='auto', target=language)\
                                            .translate(vectorizer.get_feature_names()[i])\
                                            + ' : ' + str(round(topic[i],1)))
                                            for i in topic.argsort()[:-nb_words - 1:-1]]
            bar.progress(40 + int((idx + 1) * 60 / n_components))
        else:
            latest_iteration.text(f'Saving results...  Topic {idx + 1}/{n_components}')
            results[f"Topic {idx + 1}"] = [vectorizer.get_feature_names()[i]\
                                            + ' : ' + str(round(topic[i],1))
                                            for i in topic.argsort()[:-nb_words - 1:-1]]
            bar.progress(40 + int((idx + 1) * 60 / n_components))
        st.write(f"Topic {idx + 1} : " + '\n'.join(results[f"Topic {idx + 1}"]))
    bar.progress(100)
    latest_iteration.text(f'LDA Done, results are below.')
#kept categories of products in the olist df.
dico_categories = {'All categories': 'all',
                        'bed table bath': 'cama_mesa_banho',
                        'beauty health': 'beleza_saude',
                        'sport leisure': 'esporte_lazer',
                        'computer accessories': 'informatica_acessorios',
                        'decoration furniture': 'moveis_decoracao',
                        'domestic utilities': 'utilidades_domesticas',
                        'gifts watches': 'relogios_presentes',
                        'telephony': 'telefonia',
                        'automotive': 'automotivo',
                        'toys': 'brinquedos',
                        'cool stuff': 'cool_stuff',
                        'garden tools': 'ferramentas_jardim',
                        'perfumery': 'perfumaria',
                        'babies': 'bebes',
                        'electronics': 'eletronicos',
                        'stationary store': 'papelaria',
                        'fashion bags and accessories': 'fashion_bolsas_e_acessorios',
                        'pet shop': 'pet_shop',
                        'office furniture': 'moveis_escritorio',
                        'consoles games': 'consoles_games'}

def app():
    #Loading the mining production data from Binance.
    @st.cache
    def get_cached_reviews():
        '''
        A function that gets the olist dataset from a le wagon bucket.
        '''
        df = pd.read_csv("https://wagon-public-datasets.s3.amazonaws.com/Machine%20Learning%20Datasets/reviews.csv")
        df['review_score'] = df['review_score'].map({'1':1,'2':2,'3':3,'4':4,5:5,1:1,2:2,3:3,4:4,5:5})
        #ntlk downloadings : compulsory for good deployment on Share streamlit.
        nltkDL('stopwords')
        nltkDL('punkt')
        nltkDL('wordnet')
        nltkDL('omw-1.4')
        return df

    df = get_cached_reviews()

    st.title("Natural Language Processing :")
    st.markdown('## *Demo of Latent Dirichlet Allocation*')
    st.markdown('### Definition')
    st.markdown('''*\"Latent Dirichlet allocation (LDA) is a generative probabilistic model of a
                corpus. The basic idea is that documents are represented as random mixtures over
                latent topics, where each topic is characterized by a distribution over words\"*.
                [Source](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf).
                ''')
    st.markdown('### Applications')
    st.markdown('''Basically, LDA is a tool that can be used to get the topic main topics shared
                by different texts. It is therefore quite useful to use it in customers comments
                gathered on an e-business platform to know what went wrong when they gave bad
                reviews.''')
    st.markdown('## Demo on Olist\'s Data')
    st.markdown('''Olist is a Brazilian e-commerce platform that shared some data on
                [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). We will
                use it here to find out what can create a bad review score ! ''')
    st.markdown('''I created a small tool for you to explore LDA based on the comments.
                The default settings are quite good, so you should see interesting results
                fast. ''')
    st.markdown('''Three disclaimers : \\
                - If you are using the translating feature, you might have some bugs due to
                some problems with the Google Translator API. Just click on the button again
                and the problem should disappear.\\
                - Not having the same results with the same parameters : it is perfectly normal.
                In fact, LDA models are set randomly at first and then they are fitted on the
                dataset. So, it is very likely that you will never have exactly the same results
                with the same parameters.\\
                - Remember that LDA is a simple Machine Learning tool that is not the best at this
                task. But it is very fast, as you will see with the demo. It only needs seconds
                to fit a large amount of data.''')

    #gathering info to do the LDA.
    col1, col2, col3 = st.columns(3)
    score = col1.selectbox('Which reviews score would you like to investigate ?',(1,2,3,4,5))
    category = col2.selectbox('Which category would you like to investigate ?',tuple(dico_categories.keys()))
    n_components = col3.selectbox('How many groups would you like to have ?',(2,3,4,5,6,7,8),2)
    #gathering info to do the LDA.
    col4, col5, col6 = st.columns(3)
    nb_words_per_topic = col4.selectbox('How many words do you want to show per topic ?',tuple(range(8,16)),7)
    translate_words = col5.selectbox('Do you want to translate words shown for each topic ?',('Yes','No'))
    language = col6.selectbox('Which language to you want them to be translated in ?',('en','fr'))
    data = df.copy()
    # if we want all categories we do not touch the df.
    if category != 'All categories':
        data = data[data['product_category_name'] == dico_categories[category]]
    data['review_score'] = data['review_score'].map({'1':1,'2':2,'3':3,'4':4,5:5,1:1,2:2,3:3,4:4,5:5})
    data = data[['review_score','review_comment_message']].dropna()
    data = data[data['review_score']<=score]['review_comment_message']
    my_texts = data
    my_texts = my_texts.apply(remove_punctuation)\
                    .apply(lower_txt)\
                    .apply(remove_numbers)\
                    .apply(remove_stopwords)\
                    .apply(lemmatize)
    if st.button('Launch LDA demo'):
        compute_and_show_LDA_results(data,
                                     n_components,
                                     nb_words_per_topic,
                                     translate_words=='Yes',
                                     language)
    #todo pyplot of the words?
