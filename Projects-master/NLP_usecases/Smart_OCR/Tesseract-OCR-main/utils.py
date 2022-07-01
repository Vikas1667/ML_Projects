import nltk
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import gensim.corpora as corpora

stopword_list = nltk.corpus.stopwords.words('english')
lemmitizer = WordNetLemmatizer()
lem = WordNetLemmatizer()

def read_text(path):
    with open(path,'r',encoding='utf8') as f:
        text =f.read().replace('\\n','')
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

