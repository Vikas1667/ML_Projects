import tabula
import streamlit as st
import dash
import pdfplumber
import pandas as pd

import re



def read_bank_statement_pdf_file(filename):
    try:
        tables_df=tabula.read_pdf(filename)
        return tables_df

    except Exception as e:
        print('Error in parsing or reading:',e)

def extract_data(feed):
    data = []
    with pdfplumber.open(feed) as pdf:
        pages = pdf.pages
        for p in pages:
            data.append(p.extract_tables())
    return data

def count_pdf_pages(file_path):
   rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)
   with open(file_path, "rb") as temp_file:
   return len(rxcountpages.findall(temp_file.read()))

def extract_table(pdf_path):
    tables=tabula.read_pdf(pdf_path, pages="all")
    return tables



if __name__ == "__main__":
    uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
    if uploaded_file is not None:
        # df = extract_data(uploaded_file)
        tables = extract_table(uploaded_file)

        for i in tables:
            print(i)
            print(pd.DataFrame(i))
            st.table(i)
        #     table=pd.DataFrame(i)
        #     st.table(table)
