import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import streamlit as st


def data_loader():
    uploaded_file = st.file_uploader("Choose a csv file", type=['.csv', '.xlsx', '.txt'])
    print(uploaded_file)

    if uploaded_file is not None:
        if uploaded_file.name[-4:] == 'xlsx':
            print(uploaded_file.name[0][-4:])
            df = pd.read_excel(uploaded_file,engine='openpyxl')
            st.dataframe(df)
        else:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)


def text_preprocessing():
    choice2 = ["Convert to Lower Case", "Remove Punctuation", "Convert sentence into words" ]

    choiceOperations = st.multiselect("Operations",choice2)

    out, flag = '', True
    if st.button("Process"):
        if "Convert to Lower Case" in choiceOperations:

            if flag:
                out = raw_text.lower()
                flag = False
            else:
                out = out.lower()

    st.write(out)

    if "Remove Punctuation" in choiceOperations:
        punctuations = '''!()-[]{};:'"\,>./?@#$%^&*_~'''
        if flag:

            for x in raw_text:
                if x in punctuations:
                    out = raw_text.replace(x, "")
                    flag = False
                else:
                    for x in out:
                        if x in punctuations:
                            out = out.replace(x, "")

    st.write(out)

    if "Convert sentence into words" in choiceOperations:
        if flag:
            out = raw_text.split()
            flag = False
        else:
            out = out.split()

    st.write(out)



if __name__ == '__main__':
    st.title("Text Visualizer")
    activity1 = ["Data Loader","Summarize", "Text Preprocessing"]
    choice = st.sidebar.selectbox("Select Function ",activity1)
    # data_loader()
    if choice == 'Data Loader':
        data_loader()
    if choice == 'Text Preprocessing':
        raw_text = st.text_area("Enter Text Here", "Type Here")
        text_preprocessing()
