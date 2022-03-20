import re
import numpy as np
import pandas as pd
from math import exp

import gensim

import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, precision_recall_curve

import keras
import tensorflow as tf
from keras import backend as K

from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

lemma = WordNetLemmatizer()

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Permute, Bidirectional, LSTM, Dropout, BatchNormalization,Conv1D,MaxPooling1D,LayerNormalization,Flatten
from keras.layers.embeddings import Embedding


def preprocess_text(texts):
    texts = texts.lower()
    texts = re.sub(r'[^a-zA-Z0-9]+', ' ', texts)
    splitwords = filter(lambda x: x[0] != '@', texts.split())
    splitwords = [word for word in splitwords if word not in set(stopwords.words('english'))]
    texts = " ".join(splitwords)
    return texts


def parsing_embeddings(path):
    embeddings_index = dict()
    f = open(path, encoding='utf8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    return embeddings_index


def title_embedding(title_df):
    max_len_title = title_df.X_train_title.apply(lambda x: len(x.split())).max()
    tok_title = Tokenizer()
    tok_title.fit_on_texts(title_df.X_train_title)

    vocab_size_title = len(tok_title.word_index) + 1

    encoded_title = tok_title.texts_to_sequences(title_df.X_train_title)

    padded_title = pad_sequences(encoded_title, maxlen=max_len_title, padding='post')

    title_embedding_matrix = np.zeros((vocab_size_title, 50))
    for word, i in tok_title.word_index.items():
        t_embedding_vector = embeddings_index.get(word)
        if t_embedding_vector is not None:
            title_embedding_matrix[i] = t_embedding_vector
    return max_len_title, vocab_size_title, padded_title, title_embedding_matrix


def headline_embedding(headline_df):
    max_len_headline = headline_df.X_train_headline.apply(lambda x: len(x.split())).max()
    tok_headline = Tokenizer()
    tok_headline.fit_on_texts(headline_df.X_train_headline)
    vocab_size_headline = len(tok_headline.word_index) + 1

    encoded_headline = tok_headline.texts_to_sequences(headline_df.X_train_headline)
    padded_headline = pad_sequences(encoded_headline, maxlen=max_len_headline, padding='post')
    headline_embedding_matrix = np.zeros((vocab_size_headline, 50))

    for word, i in tok_headline.word_index.items():
        h_embedding_vector = embeddings_index.get(word)
        if h_embedding_vector is not None:
            headline_embedding_matrix[i] = h_embedding_vector
    return max_len_headline, vocab_size_headline, padded_headline, headline_embedding_matrix


# Title model
def bilstm_title_model(vocab_size_title, max_len_title, title_embedding_matrix):
    title_model = Sequential()
    title_model.add(Embedding(vocab_size_title, 50, input_length=max_len_title, weights=[title_embedding_matrix], trainable=True))
    # title_model.add(Conv1D(filters=8, kernel_size=3, padding='same', activation='relu'))
    # title_model.add(MaxPooling1D(pool_size=2))

    title_model.add(Bidirectional(LSTM(20, return_sequences=True)))
    title_model.add(Dropout(0.3))
    title_model.add(BatchNormalization())
    title_model.add(Bidirectional(LSTM(20, return_sequences=True)))
    title_model.add(Dropout(0.3))
    title_model.add(BatchNormalization())
    title_model.add(Bidirectional(LSTM(20)))
    title_model.add(Dropout(0.3))
    title_model.add(BatchNormalization())
    title_model.add(Dense(64, activation='relu'))
    title_model.add(Dense(8, activation='relu'))
    title_model.add(Dense(1, activation=mod_tanh))
    title_model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])
    title_model.fit(x_train_title, Y_train_title, epochs=1, verbose=1)
    return title_model


## CNN
def CNN_model_title(vocab_size_title, max_len_title, title_embedding_matrix):
    title_model = Sequential()
    title_model.add(Embedding(vocab_size_title, 50, input_length=max_len_title, weights=[title_embedding_matrix],trainable=True))
    title_model.add(Conv1D(filters=64, kernel_size=8, activation='relu'))
    title_model.add(MaxPooling1D(pool_size=2))
    title_model.add(Flatten())

    title_model.add(Dense(8, activation='relu'))
    title_model.add(Dense(1, activation=mod_tanh))
    title_model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])
    title_model.summary()
    title_model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])
    title_model.fit(x_train_title, Y_train_title, epochs=1, verbose=1)
    return title_model

# Model for Headline
def bilstm_headline_model(vocab_size_headline, max_len_headline, headline_embedding_matrix):
    headline_model = Sequential()
    headline_model.add(Embedding(vocab_size_headline, 50, input_length=max_len_headline, weights=[headline_embedding_matrix],trainable=True))
    # headline_model.add(Conv1D(filters=8, kernel_size=3, padding='same', activation='relu'))
    # headline_model.add(MaxPooling1D(pool_size=2))

    headline_model.add((LSTM(20, return_sequences=True)))
    headline_model.add(Dropout(0.3))
    headline_model.add(BatchNormalization())
    headline_model.add((LSTM(20, return_sequences=True)))
    headline_model.add(Dropout(0.3))
    headline_model.add(BatchNormalization())
    headline_model.add((LSTM(20)))
    headline_model.add(Dropout(0.3))
    headline_model.add(BatchNormalization())
    headline_model.add(Dense(64, activation='relu'))
    headline_model.add(Dense(64, activation='relu'))
    headline_model.add(Dense(1, activation=mod_tanh))
    headline_model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])
    headline_model.fit(x_train_headline, Y_train_headline, epochs=10)

    return headline_model


def CNN_model_headline(vocab_size_headline, max_len_headline, headline_embedding_matrix):
    headline_model = Sequential()
    headline_model.add(Embedding(vocab_size_headline, 50, input_length=max_len_headline, weights=[headline_embedding_matrix],trainable=True))
    headline_model.add(Conv1D(filters=64, kernel_size=8, activation='relu'))
    headline_model.add(MaxPooling1D(pool_size=2))
    headline_model.add(Flatten())

    headline_model.add(Dense(8, activation='relu'))
    headline_model.add(Dense(1, activation=mod_tanh))

    headline_model.add(Dense(64, activation='relu'))
    headline_model.add(Dense(1, activation=mod_tanh))
    headline_model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])
    headline_model.summary()
    headline_model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])
    headline_model.fit(x_train_headline, Y_train_headline, epochs=10)
    return headline_model



def title_prediction_data_prepare(test_df):
    print('preparing title for prediction')
    # test_df['Title'] = test_df['Title'].apply(preprocess_text)
    max_len_title = test_df.Title.apply(lambda x: len(x.split())).max()

    tok_title = Tokenizer()
    tok_title.fit_on_texts(test_df.Title)
    encoded_title = tok_title.texts_to_sequences(test_df.Title)
    padded_tit = pad_sequences(encoded_title, maxlen=max_len_title, padding='post')

    return padded_tit


def headline_prediction_data_prepare(test_df):
    print('preparing headline for prediction')
    # test_df['Headline'] = test_df['Headline'].apply(preprocess_text)

    max_len_title = test_df.Headline.apply(lambda x: len(x.split())).max()

    tok_head = Tokenizer()
    tok_head.fit_on_texts(test_df.Headline)
    encoded_head = tok_head.texts_to_sequences(test_df.Headline)
    padded_h = pad_sequences(encoded_head, maxlen=max_len_title, padding='post')
    return padded_h


def mod_tanh(x):
    return K.tanh(0.6 * x)


if __name__ == '__main__':
    train_df = pd.read_csv('V:/ML_projects/InterviewTask/ZS_associate_NLP/dataset/train_file.csv')
    test_df = pd.read_csv('V:/ML_projects/InterviewTask/ZS_associate_NLP/dataset/test_file.csv')

    embedding_path = 'V:/ML_projects/InterviewTask/NLP_pipeline/pretrain_embeddings/glove.6B.50d.txt'
    submission_df=pd.DataFrame()
    # train_df['Source'] = train_df.Source.fillna(train_df["Source"].mode().iloc[0])

    X_train_title = train_df.loc[:, 'Title'].values
    y_train_title = train_df.loc[:, ['SentimentTitle']].values

    X_train_headline = train_df.loc[:, 'Headline'].values
    y_train_headline = train_df.loc[:, ['SentimentHeadline']].values

    title_df = pd.DataFrame()
    title_df['X_train_title'] = X_train_title
    title_df['y_train_title'] = y_train_title

    headline_df = pd.DataFrame()
    headline_df['X_train_headline'] = X_train_headline
    headline_df['y_train_headline'] = y_train_headline

    print('preprocess title and headline')
    # title_df['X_train_title'] = title_df.X_train_title.apply(preprocess_text)
    # headline_df['X_train_headline']=headline_df.X_train_headline.apply(preprocess_text)

    embeddings_index = parsing_embeddings(embedding_path)

    print('Creating Embeddings for the titles')
    max_len_title, vocab_size_title, padded_title, title_embedding_matrix = title_embedding(title_df)

    print('Creating Embeddings for the Headlines')
    max_len_headline, vocab_size_headline, padded_headline, headline_embedding_matrix = headline_embedding(headline_df)

    print('split the data for training and testing')
    x_train_title, x_valid_title, Y_train_title, y_valid_title = train_test_split(padded_title, y_train_title,
                                                                                  shuffle=True, test_size=0.15)

    x_train_headline, x_valid_headline, Y_train_headline, y_valid_headline = train_test_split(padded_headline,
                                                                                              y_train_headline,
                                                                                              shuffle=True,
                                                                                              test_size=0.15)

    print('training the lstm model for title')

    title_model = bilstm_title_model(vocab_size_title, max_len_title, title_embedding_matrix)
    # title_model = CNN_model_title(vocab_size_title, max_len_title, title_embedding_matrix)
    # tok = Tokenizer()
    padded_title = title_prediction_data_prepare(test_df)

    print('padded_title', padded_title)
    submission_df['IDLink'] = test_df['IDLink']
    print('title test data prepared for prediction')
    # tok = Tokenizer()

    title_prediction = title_model.predict(padded_title)
    print('title_prediction', title_prediction)

    submission_df['SentimentTitle'] = title_model.predict(padded_title)

    print('training the lstm model for headline')

    headline_model = bilstm_headline_model(vocab_size_headline, max_len_headline, headline_embedding_matrix)
    # headline_model = CNN_model_headline(vocab_size_headline, max_len_headline, headline_embedding_matrix)

    padded_head = headline_prediction_data_prepare(test_df)

    print('Headline test data prepared for prediction')

    headline_prediction = headline_model.predict(padded_head)
    print('headline_prediction', headline_prediction)

    submission_df['SentimentHeadline'] = headline_model.predict(padded_head)


    submission_df.to_csv('V:/ML_projects/InterviewTask/ZS_associate_NLP/sentiment_submissionCNNLSTM.csv')
