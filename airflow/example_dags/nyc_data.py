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


def get_data_postgres(**context):
    # Connect to PostgreSQL using PostgresHook
    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    ##get the data from the postgres table
    sql_query = """SELECT taxitype, 
                CAST(EXTRACT(YEAR FROM new_date) as INTEGER), LPAD(EXTRACT(MONTH FROM new_date)::text, 2, '0') as month
                FROM (SELECT  *, DATE((DATE_TRUNC('month', lastmonthprocessed) + INTERVAL '1 month')) AS new_date from nyc) as t"""

    result = postgres_hook.get_records(sql_query)
    # Process the result and save it in a dictionary
    data_dict = {}
    for row in result:
        key = row[0]  # Assuming the first column is the key
        year = str(row[1])
        month = str(row[2])
        Value = year + "-" + month
        data_dict[key] = Value
        context["ti"].xcom_push(key=key, value=Value)


def download_data_nyc(**context):
    def upload_to_s3(bucket_name, object_key, local_file_path, access_key_id, secret_access_key):
        s3 = boto3.client('s3',
                    endpoint_url='https://10.10.162.46:9000',
                      aws_access_key_id=access_key_id,
                      aws_secret_access_key=secret_access_key,
                      verify=False)
        try:
            s3.upload_file(local_file_path, bucket_name, object_key)
            print(f"File uploaded successfully: {local_file_path}")
        except Exception as e:
            print(f"Error uploading file: {e}")

    # Specify the bucket name, object key (file path in S3), local file path, and access credentials
    bucket_name = 'landing'
    access_key_id = '77M1DNDSRUM0WJNJIVUJ5FKCN8E4Y47OGSR7TZPJL49YM878W4T1DEFH8XH4QYJ0YJVAGDNY4OFSCYBYKIWJI1'
    secret_access_key = '98M280PJIQ7YP2FCXSKQW0ZNSLWU8A4MD20WVQFZ0K55JWVUWJDI'

    for i in ["yellow", "green", "fhv", "fhvhv"]:
        value_taxi = context["ti"].xcom_pull(task_ids="nyc_get_audit_data", key=i)
        url = "https://d37ci6vzurychx.cloudfront.net/trip-data/{}_tripdata_{}.parquet".format(
            i, value_taxi
        )
        output_file = "/mnt/shared/dfm/quarantine/{}/{}-{}.parquet".format(i,i, value_taxi)
        response = requests.get(url)
        with open(output_file, "wb") as file:
            file.write(response.content)
        upload_to_s3(bucket_name, value_taxi+'.parquet', output_file, access_key_id, secret_access_key)


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

    download_data_nyc = PythonOperator(
        task_id="download_data_nyc",
        python_callable=download_data_nyc,
        provide_context=True,
    )

    nyc_get_audit_data >> download_data_nyc
