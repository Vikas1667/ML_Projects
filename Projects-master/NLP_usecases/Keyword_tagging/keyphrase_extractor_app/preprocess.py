import nltk
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
stopword_list = nltk.corpus.stopwords.words('english')
lemmitizer = WordNetLemmatizer()


lem = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    text = text.strip()
    text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", text)
    text = text.translate(str.maketrans('','',string.punctuation))
    words = word_tokenize(text)
    text = [w for w in words if w not in stopword_list]
    text = [lem.lemmatize(word) for word in text]
    return text                 #' '.join(text)


# a = preprocess("Middle market companies face a variety of new challenges daily—including ever-increasing competition. You know that optimizing efficiency is critical for increasing profitability, but where do you start At RSM, we immerse ourselves in your business so we can gain a deeper understanding of your challenges and apply a personal approach to business optimization and efficiency. This is especially important when it comes to business optimization and efficiency. We’ll work with you to identify what can be done better, faster and at less cost. Then we’ll help you map the next steps to change.When resources are properly allocated and processes are waste-free, you can capture competitive advantage and empower your organization to take the lead—now and in the future.")
# print(a)