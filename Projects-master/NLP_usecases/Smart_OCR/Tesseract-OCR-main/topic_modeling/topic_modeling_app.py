import gensim
import nltk
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
stopword_list = nltk.corpus.stopwords.words('english')
lemmitizer = WordNetLemmatizer()
import gensim.corpora as corpora
import streamlit as st
import pyLDAvis.gensim_models
import streamlit.components.v1 as components

from pprint import pprint
lem = WordNetLemmatizer()


def read_text(path):
    with open(path,'r',encoding='utf8') as f:
        text=f.read().replace('\\n','')
    return text


def preprocess(text):
    # text = text.lower()
    text = text.strip()
    text = text.replace("\n", '')
    text = text.translate(str.maketrans('','',string.punctuation))
    words = word_tokenize(text)
    text = [w for w in words if w not in stopword_list]
    text = [lem.lemmatize(word) for word in text]
    return text


def corpus(cleaned_text):
    id2word = corpora.Dictionary([cleaned_text])
    print(id2word)
    # Create Corpus
    texts = [cleaned_text]
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    return id2word,corpus


def topicModeling(corpus,id2word,num_topics):
    # number of topics
    # num_topics = 10
    # Build LDA model
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=num_topics)

    # Print the Keyword in the 10 topics
    pprint(lda_model.print_topics())

    doc_lda = lda_model[corpus]
    return lda_model



# if __name__ =='__main__':
#     path= '../topic_modeling/input_text/text.txt'
#     inp_text=read_text(path)
#     print(inp_text)
#     preprocess_text=preprocess(inp_text)
#     print(preprocess_text)
#
#     id2word,corpus=corpus(preprocess_text)
#     print(id2word,corpus)
#
#     lda_model=topicModeling(corpus,id2word)
#
#     vis = pyLDAvis.gensim_models.prepare(topic_model=lda_model,
#                                   corpus=corpus,
#                                   dictionary=id2word)
#
#     py_lda_vis_html = pyLDAvis.prepared_data_to_html(vis)
#     components.html(py_lda_vis_html, width=1300, height=800)
