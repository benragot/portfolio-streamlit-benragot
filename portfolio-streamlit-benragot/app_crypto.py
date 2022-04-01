import streamlit as st
import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
import pandas as pd

def app():
    st.markdown('# :construction_worker: Currently being developed ! :construction_worker:')
    st.title("Ethereum mining interface")
    st.markdown('A nice interface to show how I mine Ethereum.')

    config_logging(logging, logging.DEBUG)

    key = st.secrets["BINANCE_KEY"]
    secret = st.secrets["BINANCE_SECREt_KEY"]
    client = Client(key, secret)
    option = st.slider('How many days ', 20, 200, 10)
    a = client.mining_earnings_list(algo="Ethash", userName="BRAGOT2070",pageSize=option)['data']
    df = pd.DataFrame.from_dict(a['accountProfits']).sort_values(by='time',ascending=True)
    df = df.reset_index()[['dayHashRate']]/1_000_000
    st.line_chart(df)
