import streamlit as st
from newsletter_extraction import fetch_ai_news,news_fetcher
import pandas as pd
import json
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
import requests
import feedparser
import streamlit as st
from bs4 import BeautifulSoup

st.title("NEWSLETTER APP")



# Function to get image from URL
def get_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None



def display_news_api_article(df):
    for index, row in df.iterrows():
        st.subheader(row['title'])
        st.write(f"Published at: {row['publishedAt']}")

        # Try to get and display image
        # img_url = row['url']
        # img = get_image(img_url)
        # if img is not None:
        #     st.image(img, caption=row['title'], use_column_width=True)
        # else:
        #     st.write("No image available")

        st.write(f"URL: {row['url']}")
        st.write("---")  # Add a separator between articles


def fetch_rss_feed(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        feed = feedparser.parse(response.text)
        return feed
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching RSS feed: {e}")
        return None


def extract_news(html_content):
    soup = BeautifulSoup(html_content, 'html.parser',from_encoding='utf-8')
    # Extracting the main article content
    article_content = soup.find_all('p')
    if article_content:
        # Extract the first paragraph for the main content
        main_content = article_content[0]
        title_link = main_content.find('a')
        if title_link:
            title = title_link.text
            url = title_link['href']
            description = main_content.text.replace(title_link.text, '').strip()
            return {
                'title': title,
                'url': url,
                'description': description
            }
    return None

def display_articles(feed):
    if feed:
        st.subheader("Recent News Articles")
        for entry in feed.entries:
            st.write(f"**[{entry.title}]({entry.link})**")

            # st.write(entry.description)

            extracted_news=extract_news(entry.description)

            st.write(extracted_news["description"])

            st.write("---")





if __name__ == "__main__":

    tab1, tab2 = st.tabs(["AI_News","NewsAPI"])

    with tab1:
        rss_url = "https://www.artificialintelligence-news.com/feed/"
        # # Fetch the RSS feed
        feed = fetch_rss_feed(rss_url)

        st.title("AI and Tech News")
        display_articles(feed)


    with tab2:
        st.title("Articles")
        # Load and parse the JSON data
        today_articles = news_fetcher()
        # st.write("Todays articles",today_articles)
        # Convert to DataFrame
        df = pd.DataFrame(today_articles)
        display_news_api_article(df)

        # Convert publishedAt to datetime
        df['publishedAt'] = pd.to_datetime(df['publishedAt'])

        # Display articles


        # # Display the raw data
        # st.write("Raw Data:")
        # st.write(df)


# What to do next
# Moneyview
# https://medium.com/@mihirbhalgami00/extracting-financial-data-from-moneycontrol-with-python-84f264624763
