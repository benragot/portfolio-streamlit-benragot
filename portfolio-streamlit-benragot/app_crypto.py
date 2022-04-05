'''
A module in charge of displaying the Ethereum mining interface of the streamlit.
It communicates with Binance's API to gather data and display it.
'''

from turtle import width
import streamlit as st
import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
import pandas as pd
from datetime import date
from PIL import Image

def app():
    key = st.secrets["BINANCE_KEY"]
    secret = st.secrets["BINANCE_SECRET_KEY"]
    #Loading the mining production data from Binance.
    @st.cache
    def get_cached_mining_production_data():
        '''
        A function that gets mining production data from the binance API.
        Please notcie that you have to use share streamlit secrets (TOML file) to
        '''
        config_logging(logging, logging.DEBUG)
        client = Client(key, secret)
        response = client.mining_earnings_list(algo="Ethash",
                                        userName="BRAGOT2070")['data']
        #Setting up the first date we mined Eth on Binance
        starting_time = '2021-05-16'
        starting_time = pd.to_datetime(starting_time)
        #Setting up an empty DataFrame
        df = pd.DataFrame.from_dict({'Date':[],
                                    'Average_Hash_Rate_(Mh/s)':[],
                                    'Daily_Production(Eth)':[]})
        df = df.set_index('Date')
        #Initialising the pageIndex
        pageIndex = 1
        #Filling the DataFrame
        while not starting_time in df.index:
            response = client.mining_earnings_list(algo="Ethash",
                                        userName="BRAGOT2070",
                                        pageSize=200,
                                        pageIndex=pageIndex)['data']
            df_to_concat = pd.DataFrame.from_dict(response['accountProfits'])\
                                       .sort_values(by='time',ascending=True)
            df_to_concat = df_to_concat.reset_index().drop(columns='index')
            df_to_concat['time'] = pd.to_datetime(df_to_concat['time']*1_000_000)
            df_to_concat['dayHashRate'] = df_to_concat['dayHashRate']/1_000_000
            df_to_concat = df_to_concat.rename(columns={'dayHashRate':'Average_Hash_Rate_(Mh/s)',
                                    'time':'Date',
                                    'profitAmount':'Daily_Production(Eth)'})
            df_to_concat = df_to_concat[['Date','Average_Hash_Rate_(Mh/s)','Daily_Production(Eth)']]
            df_to_concat = df_to_concat.set_index('Date')
            df = pd.concat([df,df_to_concat])
            pageIndex += 1
        #now we have a DataFrame but there are some missing dates where the hashrate was null.
        df = df.sort_index()
        today = date.today()
        starting_date = '2021-05-16'
        starting_date = pd.to_datetime(starting_date)
        idx = pd.date_range(starting_date, today)
        df = df.reindex(idx, fill_value=0)
        return df.head(len(df)-2)

    st.markdown('# :construction_worker: Currently being developed ! :construction_worker:')
    st.title("Ethereum mining interface")
    st.markdown('*A nice interface to show how I mine Ethereum.*')

    st.markdown('''## *Context*''')

    st.markdown('### What is cryptocurrency mining ?')
    st.markdown('''First of all, mining cryptocurrencies is something quite complex to explain,
                and I won't explain here how does it works, since there is plenty of information
                very well written, like this
                [short article](https://www.pcmag.com/encyclopedia/term/crypto-mining) or this
                [longer one](https://freemanlaw.com/mining-explained-a-detailed-guide-on-how-cryptocurrency-mining-works/).
                To sum up in a very simple way, it is a way to earn money by hosting computing
                power.''')

    st.markdown('### When did I start mining Ethereum and how do I do it ? ')

    st.markdown('''I started mining Ethereum in February 2021. At that time, I was mining with my
                NVIDIA RTX 2070 on my desktop PC on Windows (!). I kept mining this way, with only
                one GPU for a few months. Then, in June 2021, I decided to invest some money and
                began to buy motherboard, power supply units, risers and everything I needed to
                build my very own Ethereum mining machines, called *rigs*. There was still one
                problem : there was a big components shortage. Therefore, I bought most of them
                used and I had to deal with reliability a little bit. I learned a lot on how
                optimize production, stability and uptime of the machines.''')
    st.markdown('''Today, I have three rigs organized in a wooden structure that I built with
                a very good friend of mine, Henri. It has three levels, each with one power supply
                unit, one motherboard and four to five GPUs, as you cans see on the image below.''')
    # a little slider to adapt the size of the image.
    width_percent = st.slider('You can change the width of the image here : ', 50, 100, 50)
    st.image('images/app_crypto/rigs_structured.jpg',
             width= int(width_percent / 100 * 700),
             caption='My three rigs on the wooden structure')
    st.markdown('### Why monitoring performances ?')
    st.markdown('''Monitoring performances is crucial while mining cryptocurrencies, and there are
                many ways of doing it. In fact, for many months, I used to use an Excel File that
                I had to fill myself every day. It was not optimized so I decided to host my
                monitoring on a Streamlit interface just like this one. It is gathering
                information from the Binance API.''')
    st.markdown('### What is Binance and why do I use it ? ')
    st.markdown('''[Binance](https://www.binance.com/en) is a platform where you can buy, trade and hold many
                cryptocurrencies. Moreover, you can lend computing power to mine Ethereum, which is exactly what I do.
                It allows me to receive my earning exactly on the the platform where I will sell them. Last but not
                least, it has a nice API that I can use to show many metrics in the next section !''')
    st.markdown('## Production graphs ')
    st.markdown('### Average HashRate per day (in Mh/s)')

    if st.checkbox('You feel like tuning the dates ? Click me !'):
        starting_date = st.date_input(
        "Starting date",pd.to_datetime('2021-05-16'))
        ending_date = st.date_input(
        "Ending date")
    else:
        starting_date = pd.to_datetime('2021-05-16')
        ending_date = date.today()
    df = get_cached_mining_production_data()
    st.line_chart(df[['Average_Hash_Rate_(Mh/s)']].loc[starting_date:ending_date])

    st.markdown('### Average Eth earnings per day (in Eth)')
    if st.checkbox('You feel like tuning the dates ? Click me ! '):
        starting_date = st.date_input(
        "Starting date",pd.to_datetime('2021-05-16'))
        ending_date = st.date_input(
        "Ending date")
    else:
        starting_date = pd.to_datetime('2021-05-16')
        ending_date = date.today()
    st.line_chart(df[['Daily_Production(Eth)']].loc[starting_date:ending_date])
