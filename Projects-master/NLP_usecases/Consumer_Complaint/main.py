import pickle
import re
import nltk

from flask import Flask, jsonify, request, render_template
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
from nltk.stem import WordNetLemmatizer
nltk.download('omw-1.4')
app = Flask(__name__)

targets = {4: 'Debt collection ', 6: 'Mortgage', 3: 'Credit reporting', 2: 'Credit card', 0: 'Bank account or service ',
           1: 'Consumer Loan ', 10: "Student loan", 9: 'Prepaid card ', 8: 'Payday loan ', 5: 'Money transfers',
           7: 'Other financial service'}

clf = pickle.load(open('model.pkl', 'rb'))
loaded_vec = pickle.load(open("vectorizer.pkl", "rb"))


def pre_processing(text):
    lemmatizer = WordNetLemmatizer()
    text = text.lower()
    text = re.sub('[0-9]+', 'num', text)
    word_list = nltk.word_tokenize(text)
    word_list = [lemmatizer.lemmatize(item) for item in word_list]
    return ' '.join(word_list)


def scorer(text):
    encoded_text = loaded_vec.transform([text])
    score = clf.predict(encoded_text)
    return score


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def predict_fn():
    # text = request.get_json()['text']
    # print('input_text',text)
    text1 = request.form.to_dict()
    print(text1)
    Data = pre_processing(text1['Data'])
    print(Data)
    predictions = scorer(Data)

    # prediction = predictions.argmax(axis=0)[0]
    return render_template('results.html', result = targets.get(predictions[0]))


if __name__ == '__main__':
    app.run(debug=True)
    ## user(text)-->preprocessing()-->scorer()

