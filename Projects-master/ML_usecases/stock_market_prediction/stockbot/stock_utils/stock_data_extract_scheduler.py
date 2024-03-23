import os,sys
import pandas as pd
import datetime
import yfinance as yf
import schedule
sys.path.append('..')
from stockbot.stock_utils.lstm_model import model_train_triger
import streamlit as st

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
    date_range_string=datetime.datetime.now() - datetime.timedelta(days=180), datetime.datetime.now()

    # data=yahoo_index_data("NIFTY_FIN_SERVICE.NS")
    # data=data.rename_axis('DateTime').reset_index()
    # plot_chart(data)

    df = equity_history("NIFTY_FIN_SERVICE.NS", date_range_string[0], date_range_string[1])

    data = df.rename_axis('DateTime').reset_index()

    return data

def lstm_model_scheduler(df):

    ### from previous checkpoint retraining should be trigger
    st.write("Scheduler started")
    model=model_train_triger(df)
    model.save('..\data\stock_metadata\models/lstm_fin_nifty_prediction_latest1.keras')



