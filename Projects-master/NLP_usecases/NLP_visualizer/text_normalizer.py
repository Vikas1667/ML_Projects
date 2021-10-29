import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit
import streamlit as st
import spacy
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()
from bs4 import BeautifulSoup
import requests
import re
from string import punctuation
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer, word_tokenize
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from spacy_streamlit import visualize_ner
from sentence_transformers import SentenceTransformer, models
from sklearn.metrics.pairwise import cosine_similarity
lemma = WordNetLemmatizer()
stop_words=stopwords.words('english')
from torch import nn


@st.cache(allow_output_mutation=True)
def sentence_transformers():
    # word_embedding_model = models.Transformer('../Pretrain_model/distilbert_base_uncased/model/pytorch_model.bin', max_seq_length=128)
    word_embedding_model = models.Transformer('distilbert-base-uncased', max_seq_length=64)
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension()).to('cuda:0')
    dense_model = models.Dense(in_features=pooling_model.get_sentence_embedding_dimension(), out_features=64,
                           activation_function=nn.Tanh()).to('cuda:0')
    sent_model = SentenceTransformer(modules=[word_embedding_model, pooling_model, dense_model]).to('cuda:0')
    return sent_model


def normalize_text(text):
    # remove special characters\whitespaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', str(text), re.I | re.A)

    # lower case & tokenize text
    tokens = word_tokenize(text)

    # filter stopwords out of text
    stop_word = set(stopwords.words('english')) | set(punctuation)| set(ENGLISH_STOP_WORDS)

    # re-create text from filtered lemmatize tokens
    cleaned_text = ' '.join(lemma.lemmatize(token) for token in tokens if token not in stop_word)

    return cleaned_text


def extract_text_from_rss(rss_link):
    """
    Parses the XML and extracts the headings from the
    links in a python list.
    """
    headings = []

    # r1 = requests.get('https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms')
    r2 = requests.get(rss_link)
    # soup1 = BeautifulSoup(r1.content, features='lxml')
    soup2 = BeautifulSoup(r2.content, features='lxml')
    # headings1 = soup1.findAll('title')
    headings2 = (soup2.findAll('title'))
    print(headings2)
    # headings = headings1 + headings2
    headings=headings2

    return headings


def mmr(doc_embedding: np.ndarray, word_embeddings: np.ndarray, words, top_n, diversity):
    """Maximal Marginal Retrieval"""

    # Extract similarity within words, and between words and the document
    word_similarity = cosine_similarity(word_embeddings)
    word_doc_similarity = cosine_similarity(word_embeddings, doc_embedding)

    # Initialize candidates and already choose best keyword/keyphrase
    keywords_idx = [np.argmax(word_doc_similarity)]
    candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

    for _ in range(top_n - 1):
        # Extract similarities within candidates and between candidates and selected keywords/phrases
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)

        # Calculate MMR
        mmr = (1 - diversity) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)
        if mmr.size > 0:
            mmr_idx = candidates_idx[np.argmax(mmr)]
            # Update keywords & candidates
            keywords_idx.append(mmr_idx)
            candidates_idx.remove(mmr_idx)

    return [(words[idx], round((word_doc_similarity.reshape(1, -1)[0][idx]), 4)) for idx in keywords_idx]


def Keyword_extractor(text, cand_keys):
    # keywords = []
    word_emb, doc_emb = word_doc_embedding(text, cand_keys)
    keyword_doc = mmr(doc_emb, word_emb, cand_keys, 20, 0.5)
    # keyword_doc = ','.join([key[0] for key in keyword_doc])
    keywords = [key[0] for key in keyword_doc]
    return keywords


def word_doc_embedding(text, candidate_keys):
    sent_model=sentence_transformers()
    word_embedding = sent_model.encode(candidate_keys)
    doc_embedding = sent_model.encode([text])
    return word_embedding,doc_embedding




def keyword_extract(text_doc):
    # nlp = spacy.load("en_core_sci_sm")
    nlp = spacy.load("en_core_web_trf", disable=["tagger", "parser", "attribute_ruler", "lemmatizer"])
    doc = nlp(str(text_doc))
    visualize_ner(doc, labels=nlp.get_pipe("ner").labels)

    candKeys = [e.text for e in doc.ents]
    keywords_doc = Keyword_extractor(text_doc, candKeys)
    return [i.strip('titletitle') for i in keywords_doc]
