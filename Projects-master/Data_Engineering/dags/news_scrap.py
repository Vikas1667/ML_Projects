import requests
import numpy as np
import pandas as pd
import re
import time
from datetime import datetime, timedelta
import nltk
nltk.download('punkt')
from airflow.operators.python_operator import PythonOperator
from airflow import DAG



default_args = {
    'owner': 'Vikas',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': ['vikas.kumbharkar@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'provide_context':True
}


dag = DAG(
    'headlines',
    default_args=default_args,
    schedule_interval=timedelta(days=1))

def scrape_articles(**kwargs):
    """
    Scrape articles from one or more online newspaper sources
    Parameters
    ----------
    kwargs : dict
        Dictionary that contains all keyword arguments & values
    Returns
    -------
    sources_keywords : dict
        List of all keywords generated per source
    """
    source = kwargs['source_urls']
    r1 = requests.get(source)

    r1.status_code

    # We'll save in coverpage the cover page content
    coverpage = r1.content

    # Soup creation
    soup1 = bs4.BeautifulSoup(coverpage, 'html5lib')

    # News identification
    coverpage_news = soup1.find_all('h2', class_='linkro-darkred')
    len(coverpage_news)

    number_of_articles = 5

    # Empty lists for content, links and titles
    news_contents = []
    list_links = []
    list_titles = []

    for n in np.arange(0, number_of_articles):

        # Getting the link of the article
        link = source + coverpage_news[n].find('a')['href']
        list_links.append(link)

        # Getting the title
        title = coverpage_news[n].find('a').get_text()
        list_titles.append(title)

        # Reading the content (it is divided in paragraphs)
        article = requests.get(link)
        article_content = article.content
        soup_article = bs4.BeautifulSoup(article_content, 'html5lib')
        body = soup_article.find_all('p', class_='mol-para-with-font')

        # Unifying the paragraphs
        list_paragraphs = []
        for p in np.arange(0, len(body)):
            paragraph = body[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)

        # Removing special characters
        final_article = re.sub("\\xa0", "", final_article)

        news_contents.append(final_article)
    return news_contents


task1 = PythonOperator(
    task_id='scrape_articles',
    python_callable=scrape_articles,
    op_kwargs={'source_urls':'https://www.dailymail.co.uk'},
    dag=dag
)

