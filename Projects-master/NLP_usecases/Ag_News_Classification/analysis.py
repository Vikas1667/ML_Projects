#!/usr/bin/env python
# coding: utf-8

# # Problem Description
# ﻿AG's News Topic Classification Dataset
# 
# Version 3, Updated 09/09/2015
# 
# 
# ORIGIN
# 
# AG is a collection of more than 1 million news articles. News articles have been gathered from more than 2000  news sources by ComeToMyHead in more than 1 year of activity. ComeToMyHead is an academic news search engine which has been running since July, 2004. The dataset is provided by the academic comunity for research purposes in data mining (clustering, classification, etc), information retrieval (ranking, search, etc), xml, data compression, data streaming, and any other non-commercial activity. For more information, please refer to the link http://www.di.unipi.it/~gulli/AG_corpus_of_news_articles.html .
# 
# The AG's news topic classification dataset is constructed by Xiang Zhang (xiang.zhang@nyu.edu) from the dataset above. It is used as a text classification benchmark in the following paper: Xiang Zhang, Junbo Zhao, Yann LeCun. Character-level Convolutional Networks for Text Classification. Advances in Neural Information Processing Systems 28 (NIPS 2015).
# 
# 
# DESCRIPTION
# 
# The AG's news topic classification dataset is constructed by choosing 4 largest classes from the original corpus. Each class contains 30,000 training samples and 1,900 testing samples. The total number of training samples is 120,000 and testing 7,600.
# 
# The file classes.txt contains a list of classes corresponding to each label.
# 
# The files train.csv and test.csv contain all the training samples as comma-sparated values. There are 3 columns in them, corresponding to class index (1 to 4), title and description. The title and description are escaped using double quotes ("), and any internal double quote is escaped by 2 double quotes (""). New lines are escaped by a backslash followed with an "n" character, that is "\n".

# 
# ##  Importing Libraries

# In[5]:


import numpy as np
import pandas as pd
import csv
import os


# In[6]:


import nltk
import string, unicodedata
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import re


# In[3]:


nltk.download('punkt')


# In[7]:


from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
from sklearn.datasets import load_files
from keras import layers, models, optimizers


# ## Importing Dataset
# ### column names were included from my side as given read_me file to ease the computation 

# In[8]:


# Path_to_CSV_will_be_different_in_each_case
train_data = pd.read_csv('/home/vikas/Desktop/Vikas_Data/Projects/dishq/ag_news_csv/train.csv',names=["class index","title","description"])


# In[9]:


train_data.head(10)


# ### Delimitter Information
# #### The title and description are escaped using double quotes ("), and any internal double quote is escaped by 2 double quotes (""). New lines are escaped by a backslash followed with an "n" character, that is "\n".

# # Removing Punctuation
# #### Function for removing punctuations
#      Replacing the punctuations with no space,which in effect deletes the punctuation marks and finally returns the text stripped of punctuation marks
#     

# In[10]:


def remove_punctuation(text):
    import string
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


# In[11]:


train_data['description'] = train_data['description'].apply(remove_punctuation)
train_data['title'] = train_data['title'].apply(remove_punctuation)
train_data.head(10)


# # Extracting stopwords
# ### we have to extract the stopwords from nltk library
# ### function for removing the stopword
#     Removing the stop words and lowercasing the selected words
#     joining the list of words with space separator
#     

# In[12]:


sw = stopwords.words('english')
np.array(sw)


# In[13]:


def stopwords(text):
    text = [word.lower() for word in text.split() if word.lower() not in sw]
    return " ".join(text)


# In[14]:


train_data['description'] = train_data['description'].apply(stopwords)
train_data['title'] = train_data['title'].apply(stopwords)


# ### Features generation 

# In[15]:


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import confusion_matrix


# In[16]:


def corpus_generation():
    sent_list=[sent for sent in train_data['description']] 
    corpus=[]
    for sentence in sent_list:
        tokens=nltk.word_tokenize(sentence)
        corpus.append(tokens)
    return corpus


# In[17]:


def bag_of_words():
    print(len(train_data['description']))
    vectors=CountVectorizer(max_features=1000,min_df=3,max_df=0.6,stop_words='english')
    vect=vectors.fit_transform(train_data['description'])
    return vect


# In[18]:


def tfidf_values():
    tfidf=TfidfTransformer()
    vect=bag_of_words()
    tfidf_converted=tfidf.fit_transform(vect)
    return tfidf_converted


# ### One hot encoding 

# In[19]:


def one_hot_encoding():
    y = train_data['class index']
    y = pd.get_dummies(train_data['class index'], columns=['class index'], prefix = 'classes')
    print(np.shape(y))
    return y


# In[20]:


tfidf_converted=tfidf_values()
y=one_hot_encoding()
text_train,text_test,sent_train,sent_test=train_test_split(tfidf_converted,y,test_size=0.2,random_state=0)


# In[21]:


print(np.shape(text_train))
print(np.shape(text_test))
print(np.shape(sent_train))
print(np.shape(sent_test))


# In[22]:


def create_model_architecture(input_size):
    # create input layer 
    input_layer = layers.Input((input_size), sparse=True)
    
    # create hidden layer
    hidden_layer = layers.Dense(100, activation="relu")(input_layer)
    #hidden_layer = layers.Dense(200, activation="relu")(input_layer)
    
    # create output layer
    output_layer = layers.Dense(4, activation="sigmoid")(hidden_layer)

    classifier = models.Model(inputs = input_layer, outputs = output_layer)
    classifier.compile(optimizer=optimizers.Adam(), loss='binary_crossentropy')
    return classifier


# In[23]:


Classifier=LinearRegression()
fitting=Classifier.fit(text_train,sent_train)
sent_prediction=Classifier.predict(text_test)


# In[24]:


print(np.shape(sent_prediction))


# ## Lemmatization

# #### nltk.download('wordnet')
#   
#  

# In[25]:


nltk.download('wordnet')


# In[26]:


def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas


# In[27]:


train_data['title'].head(10)
train_data['description']=lemmatize_verbs(train_data['description'])
train_data['title']=lemmatize_verbs(train_data['description'])


# ## Spliting Dataset

# In[28]:


train_x, valid_x, train_y, valid_y = model_selection.train_test_split(train_data['description'], train_data['class index'])

# label encode the target variable 
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
valid_y = encoder.fit_transform(valid_y)

print(np.shape(train_y))
print(np.shape(valid_y))


# ## As the label contains single array nos but we have four classes, so class index should be encoded

# In[29]:


one_hot_train_data = pd.get_dummies(train_data['class index'], prefix = 'classes')
train_data['class index']=pd.get_dummies(train_data['class index'], prefix = 'classes')


# In[30]:


print(one_hot_train_data)
print(train_data.shape)
#print(valid_x.shape)
#print(valid_y.shape)
#print(train_x.shape)
print(train_data['class index'])


# ### TF-IDF Extraction¶
# ###### tf-idf weight is product of two terms: the first term is the normalized Term Frequency (TF), aka. the number of times a word appears in a document, divided by the total number of words in that document; the second term is the Inverse Document Frequency (IDF), computed as the logarithm of the number of the documents in the corpus divided by the number of documents where the specific term appears.
# 
# ##### TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
# 
# ##### IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
# ##### a. Word Level TF-IDF : Matrix representing tf-idf scores of every term in different documents
# ##### b. N-gram Level TF-IDF : N-grams are the combination of N terms together. This Matrix representing tf-idf scores of N-grams
# ##### c. Character Level TF-IDF : Matrix representing tf-idf scores of character level n-grams in the corpus
# 
# 

# In[31]:


tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=1000)
#tfidf_vect = TfidfVectorizer()


# In[32]:


vectors_convert=tfidf_vect.fit(train_data['description'])
vectors_convert=tfidf_vect.transform(train_data['description'])


# In[42]:


array=vectors_convert.todense()
array=np.array(array)
#print((array[1].shape))


# In[43]:


def create_model_architecture(input_size):
    # create input layer 
    input_layer = layers.Input((input_size), sparse=True)
    
    # create hidden layer
    hidden_layer = layers.Dense(100, activation="relu")(input_layer)
    
    # create output layer
    output_layer = layers.Dense(4, activation="sigmoid")(hidden_layer)

    classifier = models.Model(inputs = input_layer, outputs = output_layer)
    classifier.compile(optimizer=optimizers.Adam(), loss='binary_crossentropy')
    return classifier 


# In[44]:


classifier = create_model_architecture(array[1].shape)
classifier.summary()


# In[45]:


def train_model(classifier, feature_vector_train, label, feature_vector_valid, is_neural_net=False):
    # fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label,epochs=50)
    
    # predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)
    
    if is_neural_net:
        predictions = predictions.argmax(axis=-1)
    
    return metrics.accuracy_score(predictions, valid_y)


# In[46]:


#print(train_y)
one_hot_train_data = pd.get_dummies(train_y, columns=['class index'], prefix = 'classes')
#print(one_hot_train_data)
#print(cat_df_flights_onehot)


# In[47]:


# ngram level tf-idf 
tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=1000)
tfidf_vect_ngram.fit(train_data['description'])
xtrain_tfidf_ngram =  tfidf_vect_ngram.transform(train_x)
xvalid_tfidf_ngram =  tfidf_vect_ngram.transform(valid_x)


# In[48]:


accuracy = train_model(classifier, xtrain_tfidf_ngram, one_hot_train_data, xvalid_tfidf_ngram, is_neural_net=True)
print(accuracy)


# ### Limitations 
# #### Lots of Preprocessing required which is missing in above code.
# #### Feature Engineering will be considered without any comparisions.
# #### Each step verification  and Visualization of the data was not completed  due to Time Limitation.
# #### Research base was not concluded also some algorithms were not analyzed in predefined manner.
# #### Deep neural network was not fully utilized or model 
# 
# 

# ### Future Work 
# #### Research with implementation in Preprocessing part.
# #### Visualization  of  intermediate steps and Making Error free data
# #### Implementation of Deep Neural Network variations and Generating Comparative study
# #### Only 1000 features were generated as computation power was less which can be Enhanced in coming future
# #### Hyperparameter tuning and Ensembling will be also be in future work

# ### Features 
# #### Count Vectors as features
# #### TF-IDF Vectors as features
#       Word level(Used in our problem)
#       N-Gram level
#       Character level
# ####  Word Embeddings as features
# ####  Text / NLP based features
# ####  Topic Models as features

# ###  Future Models
# #### Naive Bayes Classifier
# ####  Linear Classifier
# #### Support Vector Machine
# #### Bagging Models
# #### Boosting Models(used in our problem)
# #### Shallow Neural Networks
# #### Deep Neural Networks
#      Convolutional Neural Network (CNN)
#      Long Short Term Modelr (LSTM)
#      Gated Recurrent Unit (GRU)
#      Bidirectional RNN
#      Recurrent Convolutional Neural Network (RCNN)
#      Other Variants of Deep Neural Networks
#        

# In[ ]:





# In[ ]:





# In[ ]:




