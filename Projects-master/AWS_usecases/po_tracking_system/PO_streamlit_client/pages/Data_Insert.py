import os, sys
import streamlit as st
import pandas as pd
# import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader
from PIL import Image
print(os.getcwd())
sys.path.append('../')
import mongo_test
from mongo_test import insert_data

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo


my_logo = add_logo(logo_path="./Kalika logo.png", width=300, height=60)
st.image(my_logo)


def file_upload():

    # st.header('Upload_PO_Excel for clients to Track')
    uploaded_file = st.file_uploader('Upload a file',)

    if uploaded_file is not None:
        st.write(uploaded_file)
        df = pd.read_excel(uploaded_file)
        st.write(df)

        if len(df)>0:
            # df['Due Date'] = df['Due Date'].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            df['Due Date'] = pd.to_datetime(df['Due Date'], errors='coerce')
            # st.write(df['Due Date'].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
            return df



def insert_po_details():
    po_df=pd.DataFrame()
    po_no = st.text_input("PO_Number:")
    if st.button("check if po records exist"):
        st.write(po_no)
        po_df['po_no']=po_no
        po_status_data = mongo_test.find_with_po(po_no)

        if po_status_data:
            po_data=[i for i in po_status_data]
            st.table(pd.DataFrame(po_data))
        else:
            st.write("PO records not exists proceed")
            po_df['item_no'] = st.text_input("Item_Number:", 'Enter the item number')
            po_df['SupplierItem']=st.text_input("SupplierItem:", 'Enter the Supplier item')
            po_df['ItemDescription'] = st.text_input("ItemDescription:", 'Enter the ItemDescription')

            po_df['DueDate'] = st.text_input("Due Date:", 'Enter the Due Date')
            po_df['QuantityOrdered'] = st.text_input("Quantity Ordered:", 'Enter the Quantity Ordered')
            po_df['QuantityReceived'] = st.text_input("ItemDescription:", 'Enter the Quantity Received')
            po_df['PENDING'] = st.text_input("PENDING:", 'Enter the PENDING items')
            po_df['UOM'] = st.text_input("UOM:", 'Enter the UOM')
            po_df['MaterialStatus']=st.text_input("MaterialStatus:", 'Enter the UOM')
            po_df['Transportdetails']=st.text_input("Transport details:", 'Enter the Transport details')
            st.write(po_df)
            return po_df


if __name__ == '__main__':
    uploadbtn =st.button('PO file upload')

    if "uploadbtn_state" not in st.session_state:
            st.session_state.uploadbtn_state = False

    if uploadbtn or st.session_state.uploadbtn_state:
        st.session_state.uploadbtn_state = True
        df = file_upload()

        if df is not None:
            st.write('Data Checks performing for data')
            r=mongo_test.unique_records(df)

            if len(r)>0:
                st.write('Inserting all uniques values')
                mongo_test.insert_data(r)
            else:
                st.write("All records duplicate")
                st.write('Inserting all values')
                # mongo_test.insert_data(df)


    po_b = st.button('Insert PO details')

    if "uploadbtn_state" not in st.session_state:
        st.session_state.uploadbtn_state = False


    if po_b or st.session_state.uploadbtn_state:
        st.session_state.uploadbtn_state = True
        st.write('Enter the PO details below')
        po=insert_po_details()


