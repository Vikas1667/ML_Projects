import streamlit as st
import plotly.graph_objects as go
def plot_candlestick(data):
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(x=data['DateTime'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']))

    st.plotly_chart(fig)