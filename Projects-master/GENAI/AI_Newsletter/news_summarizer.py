import requests
from bs4 import BeautifulSoup
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import faiss
import numpy as np
import streamlit as st

# Function to extract article content from a URL
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import faiss
import numpy as np


# Function to extract article content from a URL
def extract_article_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch article from {url}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Assuming the main content is within <article> tags or similar
    article = soup.find('article') or soup.find('body')  # Fallback to body if article tag is not found
    return article.get_text(separator="\n") if article else "No content found."


# Function to summarize the content using Hugging Face model
def summarize_content(content):
    # Initialize the summarization pipeline with a small model
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    # Summarize the content
    summary = summarizer(content, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']


# Function to create a FAISS index
def create_faiss_index(articles):
    # Create a FAISS index
    dimension = 768  # Example dimension size; adjust based on your embeddings
    index = faiss.IndexFlatL2(dimension)

    # Assuming you have an embedding function
    embeddings = []
    for article in articles:
        # Here you would typically convert the article to an embedding
        # For simplicity, we will use random embeddings
        embedding = np.random.random(dimension).astype('float32')
        embeddings.append(embedding)

    # Convert to numpy array and add to the index
    embeddings = np.array(embeddings)
    index.add(embeddings)

    return index


# Main function
def main():
    # Example URLs (replace with your desired URLs)
    # urls = [
    #     "https://news.google.com/rss/articles/CBMiekFVX3lxTE5LUjZTMFlNbTdocktDcURlZUViVzk0cHJxUWNuU0Y4QXdYbXpEdFpGR1NmRnVHdnc3Y1dweEw4UXd0MW1pclhNR0pUWktleS1LSm5aQU1ZYk5mS09wV2huVlhUR25YUUhsYlhYZGNYNW5QU1lJR3MxSENB?oc=5",
    #
    #     # Add more URLs as needed
    # ]
    urls=[]
    url=st.text_input("Enter the url")
    urls.append(url)
    # Extract content from the URLs
    articles = []
    if len(urls)!=0:
        for url in urls:
            content = extract_article_content(url)
            articles.append(content)

        # Create FAISS index for the articles
        index = create_faiss_index(articles)

        # Summarize each article
        for content in articles:
            print("Article Content:\n", content)
            summary = summarize_content(content)
            print("\nSummary:\n", summary)
            st.write("Article Content:\n", content)
            st.write("\nSummary:\n", summary)



# import pprint
#
# from langchain_text_splitters import RecursiveCharacterTextSplitter
#
#
# def scrape_with_playwright(urls, schema):
#     loader = AsyncChromiumLoader(urls)
#     docs = loader.load()
#     bs_transformer = BeautifulSoupTransformer()
#     docs_transformed = bs_transformer.transform_documents(
#         docs, tags_to_extract=["span"]
#     )
#     print("Extracting content with LLM")
#
#     # Grab the first 1000 tokens of the site
#     splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=1000, chunk_overlap=0
#     )
#     splits = splitter.split_documents(docs_transformed)
#
#     # Process the first split
#     extracted_content = extract(schema=schema, content=splits[0].page_content)
#     pprint.pprint(extracted_content)
#     return extracted_content
#
#
# urls = ["https://www.wsj.com"]
# extracted_content = scrape_with_playwright(urls, schema=schema)


if __name__ == "__main__":
    main()
