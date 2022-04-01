import streamlit as st
import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
import pandas as pd
from datetime import date

def app():
    key = st.secrets["BINANCE_KEY"]
    secret = st.secrets["BINANCE_SECRET_KEY"]
    #Loading the mining production data from Binance.
    @st.cache
    def get_cached_mining_production_data():
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
            df_to_concat = pd.DataFrame.from_dict(response['accountProfits']).sort_values(by='time',ascending=True)
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
        return df
    st.markdown('# :construction_worker: Currently being developed ! :construction_worker:')
    st.title("Ethereum mining interface")
    st.markdown('A nice interface to show how I mine Ethereum.')
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
