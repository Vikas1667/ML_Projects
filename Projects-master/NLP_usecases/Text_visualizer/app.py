import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import streamlit as st
# import shap
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from transformers import AutoModelForSeq2SeqLM,AutoModelWithLMHead, AutoTokenizer

import time
# from streamlit_shap import st_shap
# load_in_8bit=True
st.set_page_config(layout="wide")
from transformers import pipeline


@st.cache_resource()
def model_load():
    # load_in_8bit = True
    tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
    model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
    # tokenizer = AutoTokenizer.from_pretrained("t5-base")
    # model = AutoModelWithLMHead.from_pretrained("t5-base")
    # tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-1b7")
    # model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-1b7",load_in_8bit=True)

    return model,tokenizer

@st.cache_resource()
def flant5_model_load():
    # , load_in_8bit = True
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    return model,tokenizer

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

def summarize(text, max_length,model,tokenizer):

  input_ids = tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)

  generated_ids = model.generate(input_ids=input_ids, num_beams=2, max_length=max_length,  repetition_penalty=2.5, length_penalty=1.0, early_stopping=True)

  preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]

  return preds[0]

if __name__ == '__main__':
    st.title("Text Visualizer")

    tab1,tab2=st.tabs(["T5base","Flant5"])
    model, tokenizer = model_load()
    with tab1:
        activity1 = ["Data Loader","Summarize", "Text Preprocessing"]
        choice = st.sidebar.selectbox("Select Function ",activity1)
        # data_loader()
        if choice == 'Data Loader':
            data_loader()
        if choice == 'Text Preprocessing':
            raw_text = st.text_area("Enter Text Here", "Type Here")
            text_preprocessing()
        if choice == "Summarize":
            raw_text = st.text_area("Enter Text Here", "Type Here")
            # sum_input=text_preprocessing()

            # if raw_text:
            #     max_len = st.sidebar.slider("Select the max size", 100, 300, 50)
            #
            #     if st.button("Summarize"):
            #
            #         st.write(raw_text)
            #         start_time = time.time()
            #         summarize_text=summarize(raw_text,max_length=max_len)
            #         sum_lat_time=time.time() - start_time
            #         sum_lat_time='{0:.2f}'.format(sum_lat_time)
            #         st.sidebar.metric(label="Summary_latency", value=str(sum_lat_time)+"secs")
            #
            #         st.subheader("summarize text")
            #         st.write(summarize_text)

            if raw_text:
                max_len = st.sidebar.slider("Select the max size", 100, 300, 50)


                if st.button("Summarize"):
                    st.write(raw_text)
                    start_time = time.time()

                    summarize_text=summarize(raw_text,max_length=max_len,model=model,tokenizer=tokenizer)
                    sum_lat_time=time.time() - start_time
                    sum_lat_time='{0:.2f}'.format(sum_lat_time)
                    st.sidebar.metric(label="Summary_latency", value=str(sum_lat_time)+"secs")

                    st.subheader("summarize text")
                    st.write(summarize_text)

    with tab2:
        fmodel, ftokeizer = flant5_model_load()
        raw_text = st.text_area("Enter Text Here", key="flant5")
        if st.button("FlanT5 Summarize"):


            st.write(raw_text)
            start_time = time.time()

            summarize_text = summarize(raw_text, max_length=max_len, model=fmodel, tokenizer=ftokeizer)
            sum_lat_time = time.time() - start_time
            sum_lat_time = '{0:.2f}'.format(sum_lat_time)
            st.sidebar.metric(label="Summary_latency", value=str(sum_lat_time) + "secs")

            st.subheader("summarize text")
            st.write(summarize_text)


