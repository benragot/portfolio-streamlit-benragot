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
def app():
    #Loading the mining production data from Binance.
    @st.cache
    def get_cached_reviews():
        '''
        A function that gets the olist dataset from a le wagon bucket.
        '''
        df = pd.read_csv("https://wagon-public-datasets.s3.amazonaws.com/Machine%20Learning%20Datasets/reviews.csv")
        df['review_score'] = df['review_score'].map({'1':1,'2':2,'3':3,'4':4,5:5,1:1,2:2,3:3,4:4,5:5})
        return df

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

    df = get_cached_reviews()
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
    st.markdown('# :construction_worker: Currently being developed ! :construction_worker:')
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
                use it here to find out what creates a bad review ! ''')
    #gathering info to do the LDA.
    col1, col2, col3 = st.columns(3)
    score = col1.selectbox('Which reviews score would you like to investigate ?',(1,2,3,4,5))
    category = col2.selectbox('Which category would you like to investigate ?',tuple(dico_categories.keys()))
    n_components = col3.selectbox('How many groups would you like to have ?',(2,3,4,5))
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
    st.write(my_texts.head())
    if st.button('Launch LDA demo'):
        vectorizer = TfidfVectorizer().fit(data)
        data_vectorized = vectorizer.transform(data)
        lda_model = LatentDirichletAllocation(n_components=n_components,n_jobs=-1).fit(data_vectorized)
        def print_topics(model, vectorizer):
            for idx, topic in enumerate(model.components_):
                st.write("Topic %d:" % (idx + 1))
                st.write([(GoogleTranslator(source='auto', target='en').translate(vectorizer.get_feature_names()[i]), topic[i])
                                for i in topic.argsort()[:-5 - 1:-1]])
        print_topics(lda_model, vectorizer)
#todo pyplot of the words
