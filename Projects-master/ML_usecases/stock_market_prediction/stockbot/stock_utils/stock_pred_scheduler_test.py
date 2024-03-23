import pandas as pd
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
from nselib import capital_market
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import schedule
import os,sys
import pandas as pd
import datetime
import yfinance as yf
import schedule,time
sys.path.append('..')
from lstm_model import model_train_triger
import streamlit as st
import os,sys
# sys.path.append('..')
# from stock_data_extract_scheduler import lstm_model_scheduler
from pathlib import Path
directory=r'V:/ML_projects/github_projects/ML_projects/Projects-master/ML_usecases/stock_market_prediction/stockbot/models'

import tensorflow
import datetime

## nse site data
## can be further improvise with selenium for weekly updating list of stocks and
# download latest by using click link https://pythonexamples.org/python-selenium-click-a-link/

model_path=r'../data/stock_metadata/models/lstm_fin_nifty_prediction_01012015to02032024.keras'




dir_path=r"V:/ML_projects/StockMarket_Analysis/data/stock_metadata/"
file_path="NIFTY FINANCIAL SERVICES_Historical_PR_01012015to02032024.csv"

def equity_history(symbol,start_date,end_date):
    try:
        # start_date=date_range_string[0].strftime("%d-%m-%Y")
        # end_date=date_range_string[1].strftime("%d-%m-%Y")

        # data = capital_market.price_volume_and_deliverable_position_data(symbol=symbol, from_date=start_date,to_date=end_date)

        data = yf.download(symbol, start_date, end_date)
        # data.head()

        return data

    except Exception as e:
        return e

def data_read():

    # df=pd.read_csv(os.path.join(dir_path,file_path))
    date_range_string=datetime.datetime.now() - datetime.timedelta(days=180000), datetime.datetime.now()

    # data=yahoo_index_data("NIFTY_FIN_SERVICE.NS")

    df = equity_history("NIFTY_FIN_SERVICE.NS", date_range_string[0], date_range_string[1])

    data = df.rename_axis('DateTime').reset_index()
    # plot_chart(data)

    return data

def lstm_model_scheduler(df):

    ### from previous checkpoint retraining should be trigger
    # st.write("Scheduler started")
    try:
        print("scheduler started")
        model=model_train_triger(df)

        os.makedirs(directory,exist_ok=True)
        model_path=os.path.join(directory, 'fin_lstm_model.keras')
        model.save(model_path)
        print("Model saved at {}".format(directory))
    except Exception as e:
        print("error while schedule run")

def load_lstm_model(model_path):
    model = tensorflow.keras.saving.load_model(model_path)
    return model

def read_data(stck_path):
    nse_list=pd.read_csv(stck_path)
    # st.table(nse_list)


def equity_history(symbol,start_date,end_date):
    try:
        # start_date=date_range_string[0].strftime("%d-%m-%Y")
        # end_date=date_range_string[1].strftime("%d-%m-%Y")

        # data = capital_market.price_volume_and_deliverable_position_data(symbol=symbol, from_date=start_date,to_date=end_date)

        data = yf.download(symbol, start_date, end_date)
        # data.head()

        return data

    except Exception as e:
        # return st.write(e)
        return e

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
    # st.title("Stock Data Predictions")
    # index=st.selectbox("historical data",['Nifty',"Nifty Financial","Bank Nifty"])
    date_range_string =datetime.datetime.now() - datetime.timedelta(days=18000), datetime.datetime.now()

    # data=yahoo_index_data("NIFTY_FIN_SERVICE.NS")
    # data=data.rename_axis('DateTime').reset_index()
    # plot_chart(data)
    # st.write(date_range_string[0],date_range_string[1])

    df=equity_history("NIFTY_FIN_SERVICE.NS",date_range_string[0],date_range_string[1])

    data = df.rename_axis('DateTime').reset_index()

    plot_chart(data)
    # model=load_lstm_model(model_path)
    # st.table(data_read().head(10))
    # if st.button("Prediction"):
    #     model_pred(model,data)

    try:
        schedule.every().day.at("22:05").do(lstm_model_scheduler, df=data)
        # lstm_model_scheduler(df)

    except Exception as e:
        print("Exception occured as schedule")


    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        print("schedule is in running")
        time.sleep(1)

