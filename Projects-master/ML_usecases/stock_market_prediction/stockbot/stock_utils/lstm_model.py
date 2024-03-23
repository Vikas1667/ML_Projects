import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import numpy
import streamlit as st
import altair as alt
import tensorflow
### Create the Stacked LSTM model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from numpy import array
from datetime import date, timedelta
import plotly.graph_objects as go
import plotly.express as px





def data_prep(df):
    ### LSTM are sensitive to the scale of the data. so we apply MinMax scaler
    try:
        print("training data preparation started")
        scaler = MinMaxScaler(feature_range=(0, 1))
        df1 = scaler.fit_transform(np.array(df).reshape(-1, 1))
        # print(df1)

        ##splitting dataset into train and test split
        training_size = int(len(df1) * 0.65)
        test_size = len(df1) - training_size
        train_data, test_data = df1[0:training_size, :], df1[training_size:len(df1), :1]
        print('Train test size', training_size, test_size)
        # train_data
        return train_data,test_data

    except Exception as e:
        print('Exception as training data prep')

# convert an array of values into a dataset matrix
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    try:
        for i in range(len(dataset)-time_step-1):
            a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
            return numpy.array(dataX), numpy.array(dataY)
    except Exception as e:
        print(e)

def model_data(train_data,test_data,time_step = 100):
    print("Model Data preparation initalizing")
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, ytest = create_dataset(test_data, time_step)

    print('Train shape',X_train.shape,y_train.shape)
    print('Test_shape',X_test.shape,ytest.shape)


    # reshape input to be [samples, time steps, features] which is required for LSTM
    X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
    X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)
    return X_train,y_train,X_test,ytest


def lstm_model(X_train, y_train,X_test, ytest):
    # st.write("Moodel Training Initiated")
    try:
        print("Model Initilization")
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(100, 1)))
        model.add(LSTM(50, return_sequences=True))
        model.add(LSTM(100))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.summary()
        model.fit(X_train, y_train, validation_data=(X_test, ytest), epochs=100, batch_size=64, verbose=1)
        return model

    except Exception as e:
        print("Model Training exception",e)

def get_date(days = 8):
    days_lst = []
    today = date.today()
    retval = today
    while days > 0:
        retval += timedelta(days=1)
        if retval.weekday() not in [5,6]:
            days -= 1
            days_lst.append(retval)
    return days_lst

def prediction_data_plot(model,pred_data):

    # demonstrate prediction for next 10 days
    df = pred_data.reset_index()['Close']


    scaler = MinMaxScaler(feature_range=(0, 1))
    df = scaler.fit_transform(np.array(df).reshape(-1, 1))

    day_new = np.arange(1, 101)
    day_pred = np.arange(101, 111)

    lst_output = []
    n_steps = 100
    # x_input = pred_data[len(pred_data)-100:].reshape(1, -1)  ## fin
    x_input = df[len(df)-100:].reshape(1, -1)  ## fin
    # st.write(x_input)
    temp_input = list(x_input)
    temp_input = temp_input[0].tolist()

    # x_input.shape


    i = 0
    while (i < 10):

        if (len(temp_input) > 100):
            # print(temp_input)
            x_input = np.array(temp_input[1:])
            x_input = x_input.reshape(1, -1)
            x_input = x_input.reshape((1, n_steps, 1))
            yhat = model.predict(x_input, verbose=0)
            temp_input.extend(yhat[0].tolist())
            temp_input = temp_input[1:]
            # print(temp_input)
            lst_output.extend(yhat.tolist())
            i = i + 1
        else:
            x_input = x_input.reshape((1, n_steps, 1))
            yhat = model.predict(x_input, verbose=0)
            temp_input.extend(yhat[0].tolist())

            lst_output.extend(yhat.tolist())
            i = i + 1

    st.write("Len of lst_output",len(lst_output))

    df2=df.tolist()

    df2.extend(lst_output)
    df2 = scaler.inverse_transform(df2)

    nw=pd.DataFrame(df2,columns=['close'])
    st.write(len(nw))

    day_list=get_date(days=10)

    st.write("daylt",len(day_list))
    date_lt = []


    date_lt=pred_data['DateTime'].tolist()

    date_lt.extend(day_list)

    nw["Date"]=date_lt

    st.table(nw.tail(15))
    # st.line_chart(nw,x='Date',y="close")
    st.plotly_chart(px.line(nw,x='Date',y="close"),use_container_width=True)

def model_train_triger(df):

    df=df.reset_index()['Close']
    print(df.head(2))
    train_data,test_data=data_prep(df)

    X_train, y_train, X_test, ytest =model_data(train_data,test_data)

    model = lstm_model(X_train, y_train, X_test, ytest)
    return model

def model_pred(model,df):
    prediction_data_plot(model,df)


# def lstm_model(df):
#     model=model_train_triger(df)

# if __name__ == '__main__':
    ## load the downloaded dataset or user to get data from nse

    # df=pd.read_csv('../../data/stock_metadata/NIFTY BANK_Data.csv')
    # train_data,test_data=data_prep(df)
    # reshape into X=t,t+1,t+2,t+3 and Y=t+4
    # time_step = 100

    # X_train, y_train, X_test, ytest=model_data(train_data,test_data)


    # model=lstm_model(X_train, y_train, X_test, ytest)

    ### runs good gives option to save
