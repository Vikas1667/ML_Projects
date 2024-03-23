import pandas as pd
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
from nselib import capital_market

from plotly.subplots import make_subplots


from datetime import date, timedelta
import os,sys
sys.path.append('..')
from stockbot.stock_utils.stock_data_extract import yahoo_index_data,equity_history
from stockbot.stock_utils.lstm_model import model_pred
from stockbot.stock_utils.plot_chart import plot_candlestick

# st.write(os.getcwd(),sys.path)
import tensorflow
import datetime

## nse site data
## can be further improvise with selenium for weekly updating list of stocks and
# download latest by using click link https://pythonexamples.org/python-selenium-click-a-link/
model_path=r'../models/lstm_model.keras'
def load_lstm_model(model_path):
    model = tensorflow.keras.saving.load_model(model_path)
    return model





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
        plot_candlestick(data)

        if st.button("Prediction"):
            if os.path.exists(model_path):
                model = load_lstm_model(model_path)
                model_pred(model,data)
            else:
                st.write("model not exist train it first and save it in {}".format(model_path))





