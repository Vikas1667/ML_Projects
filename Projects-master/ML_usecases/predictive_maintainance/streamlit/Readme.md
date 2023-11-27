
## Problem
1) Predictive Maintainance
2) Remaining Useful life

## Gitrepo
https://github.com/mapr-demos/predictive-maintenance

## DB and streaming data
Instead of Mapr use streamlit

pred_maintainance_train_df

## db query
SELECT
  *
FROM
  PRED_MAINTAINANCE_TRAIN_DF
LIMIT
  10;

## Streamlit and Snowflake

https://docs.streamlit.io/knowledge-base/tutorials/databases/snowflake

## ML on snowflake
https://towardsdatascience.com/machine-learning-on-snowflake-ea6c559af2d

## MapR
MapR Streams processing more than 40,000 messages per second in this step.

### Snowflake streaming  data
### Snowpipe

https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-overview

### Snowpark

https://quickstarts.snowflake.com/guide/intro_to_machine_learning_with_snowpark_ml_for_python/index.html?index=..%2F..index&_ga=2.64845419.575280977.1700571356-457076560.1700571356#0


### snowpipe streamlit

https://medium.com/@mohitramsharma/snowflake-snowpipe-streamlit-automation-e779e5ce9984


## connection sample
streamlit_app.py
.streamlit/secrets.toml

[connections.snowflake]
account = "xxx"
user = "xxx"
password = "xxx"
role = "xxx"
warehouse = "xxx"
database = "xxx"
schema = "xxx"
client_session_keep_alive = true


Initialize connection.
conn = st.connection("snowflake")

Perform query.
df = conn.query("SELECT * from mytable;", ttl=600)

Print results.
for row in df.itertuples():
    st.write(f"{row.NAME} has a :{row.PET}:")


##
[LSTM for Predictive Maintenance on Pump Sensor Data](https://towardsdatascience.com/lstm-for-predictive-maintenance-on-pump-sensor-data-b43486eb3210)

## RUL
https://medium.com/@polanitzer/prediction-of-remaining-useful-life-of-an-engine-based-on-sensors-building-a-random-forest-in-ffad82c8a1c6
https://medium.com/@mohitramsharma/snowflake-snowpipe-streamlit-automation-e779e5ce9984
