import pandas as pd
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
from nselib import capital_market
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from datetime import date, timedelta
import os,sys
sys.path.append('..')
from stockbot.stock_utils.stock_data_extract_scheduler import data_read,lstm_model_scheduler
from stockbot.stock_utils.lstm_model import model_pred
    # st.write(os.getcwd(),sys.path)
import tensorflow
import datetime

## nse site data
## can be further improvise with selenium for weekly updating list of stocks and
# download latest by using click link https://pythonexamples.org/python-selenium-click-a-link/

model_path=r'../data/stock_metadata/models/lstm_fin_nifty_prediction_01012015to02032024.keras'
def load_lstm_model(model_path):
    model = tensorflow.keras.saving.load_model(model_path)
    return model

def read_data(stck_path):
    nse_list=pd.read_csv(stck_path)
    st.table(nse_list)


def equity_history(symbol,start_date,end_date):
    try:
        # start_date=date_range_string[0].strftime("%d-%m-%Y")
        # end_date=date_range_string[1].strftime("%d-%m-%Y")

        # data = capital_market.price_volume_and_deliverable_position_data(symbol=symbol, from_date=start_date,to_date=end_date)

        data = yf.download(symbol, start_date, end_date)
        # data.head()

        return data

    except Exception as e:
        return st.write(e)

def yahoo_index_data(symbol):
    '''

    :param symbol: nse symbol
    :return: data download

    '''
    data = yf.download(tickers=symbol, period='1d', interval='15m')
    return data

def plot_chart(data):
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(x=data['DateTime'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']))

    st.plotly_chart(fig)

if __name__ == '__main__':
    st.title("Stock Data Predictions")
    index=st.selectbox("historical data",['Nifty',"Nifty Financial","Bank Nifty"])

    if index=='Nifty Financial':
        date_range_string = st.date_input("The date is", value=(datetime.datetime.now() - datetime.timedelta(days=180), datetime.datetime.now()+timedelta(days=1)))

        data=yahoo_index_data("NIFTY_FIN_SERVICE.NS")
        data=data.rename_axis('DateTime').reset_index()
        # plot_chart(data)
        st.write(date_range_string[0],date_range_string[1])

        df=equity_history("NIFTY_FIN_SERVICE.NS",date_range_string[0],date_range_string[1])

        data = df.rename_axis('DateTime').reset_index()
        plot_chart(data)
        #
        model=load_lstm_model(model_path)

        # if st.button("Prediction"):

        model_pred(model,data)




    # data_path = "../data/stock_metadata/ind_nifty50list.csv"


    # read_data(data_path)


    #if prediction for close as well as for all other

