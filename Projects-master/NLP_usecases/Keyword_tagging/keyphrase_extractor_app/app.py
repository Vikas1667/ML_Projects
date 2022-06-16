from flask import Flask, render_template, request
from preprocess import preprocess
from keyphrase_extractor import candidate_keyword

app = Flask(__name__)
#
# @app.route('/')
# def home():
#     return render_template('index.html')


@app.route('/', methods=['GET','POST'])
def keyword_extract():
    a=[]
    if request.method == 'POST':
        print("starting")
        text = request.form['text']
        print('input',text)
        keyword_extract = preprocess(text)
        print(keyword_extract)
        a.append(keyword_extract)
    return render_template('index.html',keyword_extract=a)


if __name__== "__main__":
    app.run(debug=True)