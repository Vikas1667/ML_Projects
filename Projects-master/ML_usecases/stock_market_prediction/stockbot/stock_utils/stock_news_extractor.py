import requests
from bs4 import BeautifulSoup
import pandas as pd
import traceback
import streamlit as st

from datetime import datetime, timedelta

# Import libraries
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib.request import urlopen, Request
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import newspaper
import json


# Parameters
n = 3  # the # of article headlines displayed per ticker

# Get Data
finwiz_url = 'https://finviz.com/quote.ashx?t='
news_tables = {}
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

def news_extractor(tickers):
    for ticker in tickers:
        url = finwiz_url + ticker
        headers = {'User-Agent': user_agent }
        req = Request(url=url,headers=headers)
        st.write(req)
        resp = urlopen(req)

        html = BeautifulSoup(resp, features="lxml")
        # if html:
        #     st.markdown(html)
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table

    try:
        for ticker in tickers:
            df = news_tables[ticker]

            df_tr = df.findAll('tr')

            print('\n')

            st.write('Recent News Headlines for {}: '.format(ticker))
            # if len(df_tr)>0:
            #     st.write(df_tr)
            for i, table_row in enumerate(df_tr):
                a_text = table_row.a.text

                td_text = table_row.td.text
                td_text = td_text.strip()
                st.write(a_text, '(', td_text, ')')
                if i == n - 1:
                    break
    except KeyError:
        pass

    return news_table

# Iterate through the news
def news_parser(news_table):

    columns = ['Ticker', 'Date', 'Time', 'Headline']

    parsed_news = []
    for file_name, news_table in news_tables.items():
        for x in news_table.findAll('tr'):
            text = x.a.get_text()

            date_scrape = x.td.text.split()

            if len(date_scrape) == 1:
                time = date_scrape[0]

            else:
                date = date_scrape[0]
                time = date_scrape[1]

            ticker = file_name.split('_')[0]

            parsed_news.append([ticker, date, time, text])
    news = pd.DataFrame(parsed_news, columns=columns)
    news.to_excel(f"../data/{ticker}.xlsx")
    return news

# Sentiment Analysis
def sentiment_analysis(news,tickers):

    analyzer = SentimentIntensityAnalyzer()
    scores = news['Headline'].apply(analyzer.polarity_scores).tolist()
    df_scores = pd.DataFrame(scores)
    news = news.join(df_scores, rsuffix='_right')

    unique_ticker = news['Ticker'].unique().tolist()
    news_dict = {name: news.loc[news['Ticker'] == name] for name in unique_ticker}

    # View Data
    st.write(news)
    values = []
    for ticker in tickers:
        dataframe = news_dict[ticker]
        dataframe = dataframe.set_index('Ticker')
        dataframe = dataframe.drop(columns=['Headline'])
        print('\n')
        # print(dataframe.head())

        mean = round(dataframe['compound'].mean(), 2)
        values.append(mean)

    df = pd.DataFrame(list(zip(tickers, values)), columns=['Ticker', 'Mean Sentiment'])
    df = df.set_index('Ticker')
    df = df.sort_values('Mean Sentiment', ascending=False)
    print('\n')
    # print(df)
    # st.write(df)
    return df

def date_string_convert(date):
    new_date=datetime.strftime(date, '%Y-%m-%d')# check datetimem
    # news['Date'] = pd.to_datetime(news.Date).dt.date
    return new_date


def latest_news():
    article = newspaper.Article(url='https://finance.yahoo.com/topic/stock-market-news/')
    article.download()
    article.parse()

    article = {
        "title": str(article.title),
        "text": str(article.text),
        "authors": article.authors,
        "published_date": str(article.publish_date),
        "top_image": str(article.top_image),
        "videos": article.movies,
        "keywords": article.keywords,
        "summary": str(article.summary)
    }
    return article

# if __name__ == '__main__':
#
