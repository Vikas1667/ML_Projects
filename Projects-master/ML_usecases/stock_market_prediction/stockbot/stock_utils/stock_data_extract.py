import os,sys
import pandas as pd
import datetime
import yfinance as yf
import schedule
# sys.path.append('..')
from stock_utils.lstm_model import model_train_triger


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
        return st.write(e)


def data_read():

    # df=pd.read_csv(os.path.join(dir_path,file_path))
    date_range_string=datetime.datetime.now() - datetime.timedelta(days=180), datetime.datetime.now()

    df = equity_history("NIFTY_FIN_SERVICE.NS", date_range_string[0], date_range_string[1])

    data = df.rename_axis('DateTime').reset_index()

    return data



def yahoo_index_data(symbol):
    '''

    :param symbol: nse symbol
    :return: data download

    '''
    data = yf.download(tickers=symbol, period='1d', interval='15m')
    return data


