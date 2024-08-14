from datetime import datetime,date
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import requests
from newsapi import NewsApiClient


import sqlite3
from celery import Celery

import schedule
import time


# Constants
API_KEY = "58bcb3e309114b57a6b70ee08af15faa" # Replace with your actual API key

# Load a pre-trained SentenceTransformer model



# Function to store articles in FAISS
# def store_in_faiss(article):
    # Initialize FAISS index
    # dimension = 768  # Dimension of the embeddings (for SentenceTransformer)
    # index = faiss.IndexFlatL2(dimension)  # Use L2 distance for similarity search
    # titles = []  # To store article titles
    # embeddings = []  # To store embeddings

#   model = SentenceTransformer('all-MiniLM-L6-v2')
#     try:
#         doc = {}
#         title = article['title']
#         description = article['description']
#         url = article['url']
#         published_at = article['publishedAt']
#         # timestamp =  '2024-08-11 12:00:00'
#
#         # Create a document entry
#         doc = {
#             "title": title,
#             "description": description,
#             "url": url,
#             "publishedAt": published_at,
#             "timestamp": datetime.now().isoformat()
#         }
#
#
#         # Generate embedding for the title
#         embedding = model.encode(title)
#
#         # Store title and embedding
#         # titles.append(doc)
#
#         embeddings.append(embedding)
#
#         # Add embedding to FAISS index
#         index.add(np.array([embedding], dtype=np.float32))
#
#     except Exception as e:
#         print("Unable to Fetch or Storing in Faiss",e)
#     return doc


conn = sqlite3.connect('newsletterdb.db',check_same_thread=False)
# conn = sqlite3.connect('E:/mydatabase.db')  # Windows
cursor = conn.cursor()
# cursor.execute("DROP TABLE IF EXISTS articles;")

cursor.execute('''
CREATE TABLE IF NOT EXISTS articles (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
description TEXT,
url TEXT NOT NULL,
publishedAt TEXT,
timestamp DATETIME NOT NULL
)
''')


# Commit changes and close the connection
conn.commit()

def insert_article(doc):
    try:
        timestamp = datetime.fromisoformat(doc["timestamp"])
        # today = date.today().isoformat()
        # query = '''
        # DELETE  FROM articles WHERE DATE(timestamp) = ?
        # '''
        # cursor.execute(query, (today,))

        if timestamp.date() != date.today():
            cursor.execute('''
            INSERT INTO articles (title, description, url, publishedAt,timestamp)
            VALUES (?, ?, ?, ?, ?)
            ''', (doc['title'], doc['description'], doc['url'], doc['publishedAt'], doc['timestamp']))

            # Commit the changes
            conn.commit()
        else:
            print("Record for today already exist")
    except Exception as e:
        print(f"Insertion article in sqllite3 in DB failed{e}")

# celery_app = Celery('tasks', broker='redis://localhost:6379/0')

def document_parser(article):
    title = article['title']
    description = article['description']
    url = article['url']
    published_at = article['publishedAt']


    # Create a document entry
    doc = {
        "title": title,
        "description": description,
        "url": url,
        "publishedAt": published_at,
        "timestamp": datetime.now().isoformat()
    }

    return doc

# @celery_app.task
def fetch_ai_news():
    try:

        daily_article =[]
        newsapi = NewsApiClient(api_key=API_KEY)
        top_headlines = newsapi.get_top_headlines(
            category='technology',
            language='en',
            country='us'
        )
        articles = top_headlines['articles']

        for article in articles:

            doc=document_parser(article)
            daily_article.append(doc)
            insert_article(doc)
        return daily_article
    except Exception as e:
        print("Unable to fetch news for faiss",e)

def drop_duplicates(input_dict):
    seen = set()
    result = {}
    for key, value in input_dict.items():
        if value not in seen:
            result[key] = value
            seen.add(value)
    return result


def news_fetcher():

    ### todays news fetcher stored within db
    today = date.today().isoformat()  # Get today's date in YYYY-MM-DD format
    query = '''
    SELECT * FROM articles WHERE DATE(timestamp) = ?
    '''
    # query = '''
    # SELECT * FROM articles WHERE DATE(timestamp) = ?
    # '''

    cursor.execute(query, (today,))

    # Fetch and print today's articles
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]

    # Convert rows to a list of dictionaries
    result = []
    for row in rows:
        row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
        # row_dict = drop_duplicates(row_dict)
        result.append(row_dict)
    # print("Today's articles:",result)

    return result

import streamlit as st
if __name__ == "__main__":
    daily_article=fetch_ai_news()
    print(daily_article)
    # news_fetcher()
    # Schedule the task to run every day at 7:00 AM
    # schedule.every().day.at("23:55").do(fetch_ai_news)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
