import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import datasets
from sklearn.svm import SVC
from sklearn.metrics import auc, roc_curve

st.write("""
# Cancer Detection using Mammography
""")
dataset = pd.read_csv('Dataset.csv')

st.subheader('Data Info')
st.dataframe(dataset)
st.write(dataset.describe())

chart = st.bar_chart(dataset)
# Split data
dataset["Mass_Density"] = dataset["Mass_Density"].fillna('medium')
dataset["Shape"] = dataset["Shape"].fillna('irregular')
dataset["Margin"] = dataset["Margin"].fillna('circumscribed')
dataset = dataset.fillna(0)

# clean_dataset = pd.get_dummies(dataset, columns=['Margin', 'Mass_Density', 'Shape'])

X = dataset
y = dataset.pop('Severity')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)


def get_user_input():

    bi_rads = st.sidebar.slider('bi_rads', 0, 5, 2)
    age = st.sidebar.slider('age', 0, 130, 30)
    shape = st.selectbox("Shape", ["lobular", "round", "irregular", "round"])
    user_data= {'bi_rads': bi_rads , 'age': age, 'shape': shape}

    features = pd.DataFrame(user_data, index = [0])
    return features


user_input = get_user_input()

st.subheader(user_input)
st.write()

model = GaussianNB()
model.fit(X_train, y_train)

st.subheader('Naives bayes Model accuracy')
st.write(str(accuracy_score(y_test,model.predict(X_test))*100 + '%'))

# prediction=model.predict()
