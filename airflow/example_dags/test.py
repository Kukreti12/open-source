from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import requests
import pandas as pd
import requests
import boto3

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

def get_data_postgres():
     # Connect to PostgreSQL using PostgresHook
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    result = postgres_hook.get_records("SELECT * FROM nyc")
    # Process the result and save it in a dictionary
    data_dict = {}
    for row in result:
        key = row[0]  # Assuming the first column is the key
        value = row[1]  # Assuming the second column is the value
        data_dict[key] = value

with DAG("get_metadata", start_date=datetime(2023, 3 ,14), 
    schedule_interval="@daily",
    default_args=default_args, catchup=False,) as dag:


    nyc_get_audit_data = PythonOperator(
            task_id="nyc_get_audit_data",
            python_callable=get_data_postgres, do_xcom_push=True
    )
        

    nyc_get_audit_data