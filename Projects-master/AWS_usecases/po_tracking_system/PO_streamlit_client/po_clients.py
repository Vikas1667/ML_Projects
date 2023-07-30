import sys,os
import pandas as pd
import streamlit as st
import altair as alt
import base64
import matplotlib.pyplot as pltt
print(os.getcwd())
# V:\ML_projects\github_projects\Purchase-Order-Application\PO_streamlit_client
# from .PO_streamlit_client import mongo_test
import mongo_test

from PIL import Image

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# add_bg_from_local('tracker.jpg')


my_logo = add_logo(logo_path="./Kalika logo.png", width=300, height=60)
st.image(my_logo)
st.title("PO TRACKER")







PO = st.text_input("Enter your PO Number"," ")
Item = st.text_input("Enter your item "," ")
df_list=[]


if PO:

    plot_items=['Quantity Ordered','Quantity Shipped','Quantity Received','PENDING']
    df_list=[]
    columns = ["PO Number", "Item No", "Item Description", "Quantity Shipped"]

    if st.button("Track"):
        st.write("PO_DB connect inprogress")
        po_status_data = mongo_test.find_with_po(PO)
        st.write(po_status_data)

        df=mongo_test.records_dataframe(po_status_data)

        if len(df)>0:
            st.table(df)
            st.write(df['Material Status'])
        # if po_status_data:
        #     for k,v in po_status_data():
        #         st.write(k,"-->",v)

            # po_df=pd.DataFrame(po_status_data.items())
            # st.table(po_df)

            # Altair_Figure = alt.Chart(po_df).mark_circle().encode(
            #     x=po_df['Quantity Ordered'],
            # y = range(-5,2,100))
            # st.bar_chart(po_df,height=205,width=40)
            # st.altair_chart(Altair_Figure)
    # st.write(po_status_data)

