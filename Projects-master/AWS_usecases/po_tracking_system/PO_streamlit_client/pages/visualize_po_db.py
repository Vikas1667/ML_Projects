import pandas as pd
import pygwalker as pyg
import os, sys
import streamlit.components.v1 as components
import streamlit as st

sys.path.append('../')
import mongo_test
from mongo_test import insert_data

df=mongo_test.find_mongo()

gwalker = pyg.walk(df,return_html=True)

components.html(gwalker, height=1000, scrolling=True)