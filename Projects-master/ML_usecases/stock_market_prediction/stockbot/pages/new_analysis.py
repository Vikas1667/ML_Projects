import streamlit as st
from stock_utils.stock_news_extractor import *
import numpy as np

ticker_list = np.load(r"V:\ML_projects\StockMarket_Analysis\data\stock_metadata\finviz_ticker.npy", allow_pickle=True)

search_query = 'TCS'
# df=star_new_crawler(page, search_query, limit)
# st.table(df)

if __name__ == '__main__':
    tab1, tab2 = st.tabs(["Latest_news", "ticker_based"])
    with tab2:

        tk=st.multiselect("Select the ticker to extract",ticker_list)
        if tk:
            st.write(tk)
            news_extract=news_extractor(tk)
            parsed_news=news_parser(news_extract)
            df=sentiment_analysis(parsed_news,tk)
            st.table(df)


    ## tab creation
    with tab1:
        article=latest_news()
        st.write(article)

