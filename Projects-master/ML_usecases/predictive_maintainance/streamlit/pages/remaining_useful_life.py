import streamlit as st
import numpy as np
import pandas as pd
import os
from sklearn import preprocessing
from keras.models import Sequential,load_model
import streamlit as st
min_max_scaler = preprocessing.MinMaxScaler()

sequence_length = 50
sensor_cols = ['s' + str(i) for i in range(1,22)]
sequence_cols = ['setting1', 'setting2', 'setting3', 'cycle_norm']
sequence_cols.extend(sensor_cols)

def data_prep(test_df):
    test_df.drop(test_df.columns[[26, 27]], axis=1, inplace=True)
    test_df.columns = ['id', 'cycle', 'setting1', 'setting2', 'setting3', 's1', 's2', 's3',
                       's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14',
                       's15', 's16', 's17', 's18', 's19', 's20', 's21']
    test_df['cycle_norm'] = test_df['cycle']
    cols_normalize = test_df.columns.difference(['id', 'cycle', 'RUL', 'label1', 'label2'])

    norm_test_df = pd.DataFrame(min_max_scaler.fit_transform(test_df[cols_normalize]),
                                columns=cols_normalize,
                                index=test_df.index)
    test_join_df = test_df[test_df.columns.difference(cols_normalize)].join(norm_test_df)
    test_df = test_join_df.reindex(columns=test_df.columns)
    test_df = test_df.reset_index(drop=True)
    return test_df


def r2_keras(y_true, y_pred):
    """Coefficient of Determination
    """
    SS_res = K.sum(K.square( y_true - y_pred ))
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) )
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )


def rul(test_df):
    seq_array_test_last = [test_df[test_df['id'] == id][sequence_cols].values[-sequence_length:]
                           for id in test_df['id'].unique() if len(test_df[test_df['id'] == id]) >= sequence_length]

    seq_array_test_last = np.asarray(seq_array_test_last).astype(np.float32)


    return seq_array_test_last

if __name__ == "__main__":
    st.title('BlueCloud Streamlit App for Predictive maintainance')
    model_path = 'V:/ML_projects/github_projects/predictive-maintenance/notebooks/jupyter/Output/regression_model.h5'
    test_df = pd.read_csv(r'V:/ML_projects/github_projects/predictive-maintenance/notebooks/jupyter/Dataset/PM_test.txt', sep=" ", header=None)
    estimator = load_model(model_path,custom_objects={'r2_keras': r2_keras})
    df=data_prep(test_df)
    seq_array_test_last=rul(df)
    y_pred_test = estimator.predict(seq_array_test_last)
    st.write(y_pred_test)
