import pandas as pd
import streamlit as st
from spacy_streamlit import visualize_ner
from text_normalizer import normalize_text, extract_text_from_rss,keyword_extract
from torch import nn
from transformers import pipeline
import string
import en_core_web_sm
nlp = en_core_web_sm.load()

def data_loader():
    uploaded_file = st.file_uploader("Choose a csv file", type=['.csv', '.xlsx', '.txt'])
    print(uploaded_file)

    if uploaded_file is not None:
        if uploaded_file.name[-4:] == 'xlsx':
            print(uploaded_file.name[0][-4:])
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.dataframe(df)

        else:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)


def text_preprocessing():
    choice2 = ["Convert to Lower Case", "Remove Punctuation", "Convert sentence into words"]

    choiceOperations = st.multiselect("Operations", choice2)

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
        punctuations = '''!()-[]{};:'"\,>./?#$%^&*_~!'''
        str_punctuation=string.punctuation
        print('str punctuation',str_punctuation)

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


# Function to take in dictionary of entities, type of entity, and returns specific entities of specific type
def entRecognizer(entDict, typeEnt):
    entList = [ent for ent in entDict if entDict[ent] == typeEnt]
    return entList

def summarize():
    text_to_summarize = st.text_input("Add your RSS link here!", "https://www.moneycontrol.com/rss/buzzingstocks.xml")
    fin_headings = extract_text_from_rss(text_to_summarize)
    summarizer = pipeline("summarization")
    fin_headings=normalize_text(fin_headings)
    fin_headings=fin_headings.strip('title')
    summarized = summarizer(fin_headings, min_length=75, max_length=200)
    st.write(summarized)
    st.write(fin_headings)


if __name__ == '__main__':
    st.title("Text Visualizer")
    activity1 = ["Data Loader", "Summarize", "Text Preprocessing", "NER", "KeyWord_extractor"]
    choice = st.sidebar.selectbox("Select Function ", activity1)

    # data_loader()
    if choice == 'Data Loader':
        data_loader()
    if choice == 'Summarize':
        summarize()


    if choice == 'Text Preprocessing':
        raw_text = st.text_area("Enter Text Here", "Type Here")
        text_preprocessing()
    if choice == 'NER':
        # Getting Entity and type of Entity
        entities = []
        entityLabels = []
        user_input = st.text_input("Add your RSS link here!", "https://www.moneycontrol.com/rss/buzzingstocks.xml")
        fin_headings = extract_text_from_rss(user_input)
        print(fin_headings)

        # display the news in an expander section
        with st.expander("Expand for xNews!"):
            for h in fin_headings:
                st.markdown("* " + h.text)

        fin_headings = ''.join([normalize_text(i) for i in fin_headings])
        doc = nlp(fin_headings)

        visualize_ner(doc, labels=nlp.get_pipe("ner").labels)

        # raw_text = st.text_input('Enter text')
        # doc = nlp(raw_text)

    if choice=="KeyWord_extractor":
        user_input = st.text_input("Add your RSS link here!", "https://www.moneycontrol.com/rss/buzzingstocks.xml")
        fin_headings = extract_text_from_rss(user_input)

        with st.expander("Expand for RSS feeds!"):
            for h in fin_headings:
                st.markdown("* " + h.text)

        fin_headings = ''.join([normalize_text(i) for i in fin_headings])
        print('fin_headings',fin_headings)

        keyword_doc = keyword_extract(fin_headings)
        st.write(keyword_doc)

        raw_text = st.text_input("Add your text")

        if raw_text:
            clean_text=normalize_text(raw_text)
            keyword_doc = keyword_extract(clean_text)
            st.write(keyword_doc)
