import pandas as pd
import streamlit as st

# sys.path.insert(1, r"V:\ML_projects\StockMarket_Analysis\stockbot\stock_utils")
# st.write(sys.path)
from pages.stock_utils.account_analysis import profit_loss
from utils import *

st.title('Trade account analysis')


if __name__ == "__main__":

    upload_file = st.file_uploader("Choose a file")
    st.write(upload_file)


    if upload_file is not None:
        file_ext = upload_file.name.split('.')[1]
        if file_ext == 'xlsx':
            df = pd.read_excel(upload_file,sheet_name='F&O PNL')
            st.dataframe(df)
            st.markdown(df.columns)
        else:
            df = pd.read_csv(upload_file)
            df = st.dataframe(df)
            st.markdown(df.columns)
        a=profit_loss(df,10)
        a.profit_loss_chart()

    with st.sidebar:
        st.write('Blocks')
        if st.button("Email_analysis"):
            email_extractor()
