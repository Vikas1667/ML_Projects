import requests
import numpy as np
import faiss
from datetime import datetime
from flask import render_template
from sentence_transformers import SentenceTransformer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from newsapi import NewsApiClient

import webbrowser

API_KEY = "58bcb3e309114b57a6b70ee08af15faa" # Replace with your actual API key
NEWS_API_URL = "https://newsapi.ai/v1/articles"  # Example endpoint for AI news
# app = Flask(__name__)
# Function to store articles in FAISS


def store_in_faiss(article):
    title = article['title']
    description = article['description']
    url = article['url']
    published_at = article['publishedAt']
    timestamp = datetime.now().isoformat()

    # Create a document entry
    doc = {
        "title": title,
        "description": description,
        "url": url,
        "publishedAt": published_at,
        "timestamp": timestamp
    }

    # Generate embedding for the title
    embedding = model.encode(title)

    # Store title and embedding
    titles.append(doc)
    embeddings.append(embedding)

    # Add embedding to FAISS index
    index.add(np.array([embedding], dtype=np.float32))

# Function to fetch AI news
def fetch_ai_news():
    try:

        newsapi = NewsApiClient(api_key=API_KEY)
        top_headlines = newsapi.get_top_headlines(
            category='technology',
            language='en',
            country='us'
        )
        articles = top_headlines['articles']
        titles=[]


        for article in articles:
            title = article['title']
            description = article['description']
            url = article['url']
            published_at = article['publishedAt']
            timestamp = datetime.now().isoformat()
            # Create a document entry
            doc = {
                "title": title,
                "description": description,
                "url": url,
                "publishedAt": published_at,
                "timestamp": timestamp
            }
            titles.append(doc)

        # print(response.json())
        print(titles)

        with open('saving.txt', 'w') as f:
            for i in titles:
                f.write('%s\n' % i)

        # html_content = render_template('newsletter.html', articles=titles)
        # print(html_content)

        # with open('saving.html', 'wb+') as f:
        #     f.write(html_content)
        #
        # webbrowser.open('saving.html')

        # for article in articles:
        #     store_in_faiss(article)
    except Exception as e:
        print("Unable to fetch news for faiss",e)


if __name__ == "__main__":
    fetch_ai_news()