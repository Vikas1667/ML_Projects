import streamlit as st
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from embedchain import App as EmbedChainApp
import os
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "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"

config = {
  'llm': {
    'provider': 'huggingface',
    'config': {
      'model': 'mistralai/Mistral-7B-Instruct-v0.2',
      'top_p': 0.5
    }
  },
  'embedder': {
    'provider': 'huggingface',
    'config': {
      'model': 'sentence-transformers/all-mpnet-base-v2'
    }
  }
}
# Content Collection using LangChain
def collect_content(urls):
    documents = []
    for url in urls:
        loader = WebBaseLoader(url)
        documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    return texts


# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Store in FAISS using LangChain
def store_in_faiss(texts):
    return FAISS.from_documents(texts, embeddings)


# EmbedChain for additional content
embed_chain_app = EmbedChainApp.from_config(config=config)


# Streamlit App
def app(faiss_db):
    st.title("Newsletter Content Pipeline")

    # Search existing content
    query = st.text_input("Search for content:")
    if query:
        results = faiss_db.similarity_search(query, k=5)
        for doc in results:
            st.write(doc.page_content)
            st.write(f"Source: {doc.metadata['source']}")
            st.write("---")

    # Add new content
    new_url = st.text_input("Add new website content:")
    if new_url:
        with st.spinner("Adding new content..."):
            embed_chain_app.add(new_url, data_type="web_page")
            st.success("Content added successfully!")

    # Query EmbedChain
    embed_query = st.text_input("Query EmbedChain:")
    if embed_query:
        response = embed_chain_app.query(embed_query)
        st.write("EmbedChain Response:")
        st.write(response)


if __name__ == "__main__":
    urls = [
        "https://www.artificialintelligence-news.com/categories/ai-applications/ai-chatbots/",
        "https://www.artificialintelligence-news.com/",
        # Add more URLs as needed
    ]

    texts = collect_content(urls)
    faiss_db = store_in_faiss(texts)
    app(faiss_db)