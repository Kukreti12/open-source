from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.bash_operator import BashOperator
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


def get_data_postgres(**context):
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
        Value=year+"-"+month
        data_dict[key]=Value
        context['ti'].xcom_push(key=key, value=Value)
        print(key, year, month)


def download_data_nyc(**context):
    value_yellow = context['ti'].xcom_pull(task_ids='nyc_get_audit_data', key='yellow')
    for i in ['yellow','green','fhv','fhvhv']:
        url = "https://d37ci6vzurychx.cloudfront.net/trip-data/{}_tripdata_{}.parquet".format(i,value_yellow)
        output_file = "/mnt/shared/DFM/quarantine/{}-{}.parquet".format(i,value_yellow)
        response = requests.get(url)
        with open(output_file, "wb") as file:
            file.write(response.content)
        context['ti'].xcom_delete(key=i)
with DAG(
    "get_metadata",
    start_date=datetime(2023, 3, 14),
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,) as dag:

    nyc_get_audit_data = PythonOperator(
        task_id="nyc_get_audit_data",
        python_callable=get_data_postgres,
        provide_context=True,
    )

    download_data_nyc = PythonOperator(
    task_id="download_data_nyc",
    python_callable=download_data_nyc,
    provide_context=True,
    )

  
    nyc_get_audit_data >> download_data_nyc
