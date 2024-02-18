import os, sys
import streamlit as st
import pandas as pd
# import streamlit_authenticator as stauth
# import yaml
import time

import random
# from yaml.loader import SafeLoader
from PIL import Image
print(os.getcwd())
sys.path.append('../')
import mongo_test
from mongo_test import insert_data,update_records

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo


my_logo = add_logo(logo_path="./Kalika logo.png", width=300, height=60)
st.image(my_logo)



po_update =st.button('Update Current Status for PO')

if "uploadbtn_state" not in st.session_state:
    st.session_state.uploadbtn_state = False


if po_update or st.session_state.uploadbtn_state:
    st.session_state.uploadbtn_state = True

    updated_placeholder =[]
    updated_df=pd.DataFrame()
    PO = st.text_input("Enter your PO Number to Search", "")
    if PO:
        po_status_data = mongo_test.find_with_po(PO)

        if po_status_data:
            st.write(po_status_data)
            df = mongo_test.records_dataframe(po_status_data)
            st.write('Update the values')
            val =['Quantity Shipped', 'Material Status', "Transport details "]
            item_details=['Supplier Item',"Item No","Due Date"]
            key = time.time()
            widget_id = (id for id in range(1, 100_00))
            # df=df.fillna("NOT")
            st.table(df)
            query_update_dict=[]
            for i,v in zip(item_details,val):
                ma_ = st.checkbox(v)
                key = time.time()
                if ma_:
                    updated_placeholder.append(v)
                    for ind,val in df.iterrows():
                        col1,col2 = st.columns(2)
                        with col1:
                            st.write('current value for {} is :-->{}'.format(val[i],val[v]))
                        with col2:
                            new_value=st.text_input('update value',key =next(widget_id))
                            st.write(new_value)
                            if new_value!=None and new_value!='':
                                update_tup=(v,val[v],new_value)
                                query_update_dict.append(update_tup)

            if st.button('Update Records',key=next(widget_id)):
                st.write(len(query_update_dict))
                for k in query_update_dict:
                    st.write(k)
                    st.write('case',k[0])
                    query = {k[0]:k[1]}  ## issue
                    update = {"$set": {k[0]: k[2]}}
                    updated_msg=update_records(query,update,PO)
                    st.write(updated_msg)



            if po_status_data:
                st.write(po_status_data)
