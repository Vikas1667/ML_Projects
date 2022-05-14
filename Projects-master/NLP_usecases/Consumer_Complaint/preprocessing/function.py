import re

import nltk
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
from nltk.stem import WordNetLemmatizer
nltk.download('omw-1.4')

stemmer = nltk.stem.SnowballStemmer('english')
stop_words = set(nltk.corpus.stopwords.words('english'))


def tokenize(text):
    text = text.lower()
    tokens = [word for word in nltk.word_tokenize(text)]
    lem = WordNetLemmatizer()
    stemmed_text = ' '.join([lem.lemmatize(item) for item in tokens if (item not in stop_words)])
    return stemmed_text
