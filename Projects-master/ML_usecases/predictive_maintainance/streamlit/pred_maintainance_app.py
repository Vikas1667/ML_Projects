import streamlit as st
import snowflake.connector
import pandas as pd

from keras.models import Sequential,load_model

model_path = './Output/regression_model.h5'

# estimator = load_model(model_path, custom_objects={'r2_keras': r2_keras})

# your_username
# COMPUTE_WH	BLUECLOUD_IOT	PUBLIC
def create_snowflake_connection():
    conn = snowflake.connector.connect(

    )
    return conn


def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor


def fetch_data_as_dataframe(connection, query):
    cursor = execute_query(connection, query)
    data = cursor.fetch_pandas_all()
    return data


if __name__ == "__main__":
    # Example query
    query = "SELECT * FROM BLUECLOUD_IOT.PUBLIC.SENSOR_DATA LIMIT 10"

    # Connect to Snowflake
    # snowflake_conn = create_snowflake_connection()

    # Fetch data
    # result_df = fetch_data_as_dataframe(snowflake_conn, query)

    # Print or use the result_df in your Streamlit app

    st.title('BlueCloud Streamlit App for Predictive maintainance')
    # st.table(result_df)








