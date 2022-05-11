from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
import datetime
import pendulum

default_args = {
    'owner': 'Vikas',
    'depends_on_past': False,
    'start_date': datetime.datetime(2022, 5, 29),
    }


# Defining the DAG using Context Manager
with DAG(
        'extract-meeting-activities',
        default_args=default_args,
        schedule_interval=None,
        ) as dag:
        t1 = BashOperator(
                task_id = 'extract_text_from_pdf',
                bash_command='V:/ML_projects/Airflow/dags/pdf_to_text.sh {{ dag_run.conf["pdf_filename"]}}',
        )

        t2 = BashOperator(
                task_id = 'extract_metadata_from_text',
                bash_command ='python3 V:/ML_projects/Airflow/dags/extract_metadata.py',
        )

        t1 >> t2 # Defining the task dependencies