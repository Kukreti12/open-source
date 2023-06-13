from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import XCom
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
    "retry_delay": timedelta(minutes=5),
}


def get_data_postgres():
    # Connect to PostgreSQL using PostgresHook
    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    ##get the data from the postgres table
    sql_query = """SELECT taxitype, 
                EXTRACT(YEAR FROM new_date) as year, LPAD(EXTRACT(MONTH FROM new_date)::text, 2, '0') as month
                FROM (SELECT  *, DATE((DATE_TRUNC('month', lastmonthprocessed) + INTERVAL '1 month')) AS new_date from nyc) as t"""

    result = postgres_hook.get_records(sql_query
    )
    # Process the result and save it in a dictionary
    data_dict = {}
    for row in result:
        key = row[0]  # Assuming the first column is the key
        year = str(row[1])
        month = str(row[2])
        data_dict[key]=year+"-"+month
        # context['ti'].xcom_push(key=key, value=value)
        print(key, year, month)


with DAG(
    "get_metadata",
    start_date=datetime(2023, 3, 14),
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:
    nyc_get_audit_data = PythonOperator(
        task_id="nyc_get_audit_data",
        python_callable=get_data_postgres,
        provide_context=True,
    )

    nyc_get_audit_data
