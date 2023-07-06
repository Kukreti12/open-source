from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import requests
import pandas as pd
import requests
from sqlalchemy import create_engine
import boto3

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def download_rates():
    # Specify the API endpoint URL
    url = "https://api.wazirx.com/sapi/v1/tickers/24hr"
    # Make an HTTP GET request to the API
    response = requests.get(url)

    # Parse the response content as JSON and store it in a Python object
    data = response.json()
    df = pd.DataFrame(data)
    df.columns = map(str.lower, df.columns)
    csv_path = "/mnt/shared/DFM/file.csv"
    df.to_csv(csv_path, index=False)
    # Connect to PostgreSQL using PostgresHook
    # postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    # # Push the DataFrame to a table in PostgreSQL
    # table_name = "test1"
    # postgres_hook.insert_rows(table_name, df.values.tolist(), df.columns.tolist())


def s3_upload():
    s3_resource = boto3.resource ("s3",
        endpoint_url="https://10.10.162.46:9000",
        access_key_id = '77M1DNDSRUM0WJNJIVUJ5FKCN8E4Y47OGSR7TZPJL49YM878W4T1DEFH8XH4QYJ0YJVAGDNY4OFSCYBYKIWJI1',
        secret_access_key = '98M280PJIQ7YP2FCXSKQW0ZNSLWU8A4MD20WVQFZ0K55JWVUWJDI',
        verify=False,
       )

    # Upload your file from DF location to the S3 bucket
    s3_resource.Bucket("landing").upload_file(
        "/mnt/shared/DFM/file.csv", "file.csv"
    )


with DAG(
    "ingestion",
    start_date=datetime(2023, 3, 14),
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:
    push_data_df_postgres = PythonOperator(
        task_id="downloading_rates", python_callable=download_rates
    )

    s3_upload = PythonOperator(task_id="s3_upload", python_callable=s3_upload)

    push_data_df_postgres >> s3_upload
