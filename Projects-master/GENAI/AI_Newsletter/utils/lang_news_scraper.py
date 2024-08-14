import pprint
import asyncio
from typing import List, Dict
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from playwright.async_api import async_playwright
from transformers import pipeline

# Initialize the text-to-text pipeline with flan-t5-large
extractor = pipeline("text2text-generation", model="google/flan-t5-large", device="cpu")


def extract(content: str, schema: Dict) -> List[Dict]:
    prompt = f"""
    Extract the following information from the given text:
    - news_article_title
    - news_article_summary

    Text: {content}

    Respond in the following JSON format:
    {{
        "news_article_title": "extracted title",
        "news_article_summary": "extracted summary"
    }}
    """

    result = extractor(prompt, max_length=500, do_sample=False)[0]['generated_text']

    # Basic parsing of the generated JSON-like string
    extracted = {}
    for line in result.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().strip('"')
            value = value.strip().strip(',').strip('"')
            extracted[key] = value

    return [extracted]


# async def get_images(url):
#     async with async_playwright() as p:
#         browser = await p.chromium.launch()
#         page = await browser.new_page()
#         await page.goto(url)
#
#         images = await page.query_selector_all('img')
#         image_srcs = []
#         for img in images:
#             src = await img.get_attribute('src')
#             if src and src.startswith('http'):
#                 image_srcs.append(src)
#
#         await browser.close()
#     return image_srcs


def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["span", "p", "h1", "h2", "h3", "img"]
    )
    print("Extracting content with Hugging Face model")

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)

    extracted_content = extract(content=splits[0].page_content, schema=schema)

    # Get images
    # image_srcs = await get_images(urls[0])

    # Add image URLs to extracted content
    for item in extracted_content:
        if image_srcs:
            item['image_url'] = image_srcs[0]  # Use the first image
            image_srcs = image_srcs[1:]  # Remove the used image

    pprint.pprint(extracted_content)
    return extracted_content


schema = {
    "properties": {
        "news_article_title": {"type": "string"},
        "news_article_summary": {"type": "string"},
        "image_url": {"type": "string"},
    },
    "required": ["news_article_title", "news_article_summary"],
}

urls = ["https://www.wsj.com"]

#
# def run_scraper():
#     # Create a new event loop
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     try:
#         return loop.run_until_complete(scrape_with_playwright(urls, schema=schema))
#     finally:
#         loop.close()


# Run the scraper
st.title("News Scrapper")
extracted_content = scrape_with_playwright(urls,schema)
st.write(extracted_content)
