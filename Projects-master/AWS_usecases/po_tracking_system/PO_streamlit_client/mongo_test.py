
import pymongo
from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
import streamlit as st
import pandas as pd
import json
from urllib.parse import quote_plus

# Create a new client and connect to the server
samp_data_path='sample_data/28 JUNE 2023 CFS.xlsx'

uri = ""
# connect=False

@st.experimental_singleton()
def init_connection():
    return MongoClient(uri,connect=False)


client = init_connection()
try:
    client.admin.command('ping')
    st.write("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Connection issue ", e)

mng_db = client['kalika_data']
collection_name='kalika_po'


# admin_collection_name = 'po_admin'
# db_cm = mng_db[admin_collection_name]
db_cm = mng_db[collection_name]

# db_cm.create_index("PO Number")


def find_mongo():

    records = db_cm.find()
    df=pd.DataFrame(list(records))
    return df

def insert_data(df):
    try:
        print("DB verified")
        # df=pd.read_excel(path)
        data_json = json.loads(df.to_json(orient='records'))
        print(data_json)
        # db_cm.remove()
        db_cm.insert_many(data_json)
    except Exception as e:
        print(e)


# Send a ping to confirm a successful connection


def find_with_po(po_number):
    try:
        # result = db_cm.find_one({"PO Number":po_number})
        db_cm = mng_db[collection_name]
        result = db_cm.find({'PO Number': po_number})

        if result:
            st.write("Results:",result)
            return result
        else:
            return "No document Found with PO number{}".format(po_number)
    except Exception as e:
        return "Connection error due to{}".format(e)


def records_dataframe(po_status_data):
    df_list=[]
    if po_status_data:
        for doc in po_status_data:
            # st.write('doc ',doc)
            df_list.append(doc)
        df = pd.DataFrame(df_list)
        return df

def unique_records(df,key='PO'):

    po_list=df['PO Number'].tolist()
    r=db_cm.find()
    po_df=pd.DataFrame(list(r))

    if len(po_df)>0:
        po_dup=po_df[po_df['PO Number'].isin(po_list)]
        st.write("Records already exists for below PO",po_dup)
        po_unq = po_df[~po_df['PO Number'].isin(po_list)]
        return po_unq

    else:
        st.write("No Duplicate or new records are detected")
        return po_df


def update_records(query,updated_val,po):

    try:
            
        db_cm.update(query,updated_val)
        po_status_data = find_with_po(po)
        df = records_dataframe(po_status_data)
        st.write('Updated the values', df)

        return "Update successful"

    except Exception as e:
        st.write('Update issue')
