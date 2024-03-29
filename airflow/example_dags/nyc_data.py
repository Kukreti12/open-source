from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import XCom
from datetime import datetime, timedelta
import requests
import pandas as pd
import requests
import boto3
from airflow.utils.db import provide_session
default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}



@provide_session
def cleanup_xcom(session=None):
    session.query(XCom).filter(XCom.dag_id == "get_nyc_taxi_data").delete()

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
    access_key_id = 'QCRTMKOGJAXQBXYZVKW0P3YVVFUTF40WGGYRYI2QXF8A1M37VR5EZOVGDBBJ4SQX7SASJJTA12IF2XVXHBHQO2GSSMT6WW4BBUKSZ0WG1S5J1'
    secret_access_key = 'E2BCPBXXGKKHSL531C5L2YYWQQ8Y5UEM8B6OY21QJYPMHU9P1UA5EZHYQ6PZQWUJTWYXR8CJ8X5LV20FSCR8D4J0HW'

    for i in ["yellow", "green", "fhv", "fhvhv"]:
        value_taxi = context["ti"].xcom_pull(task_ids="pull_month_to_be_processed", key=i)
        url = "https://d37ci6vzurychx.cloudfront.net/trip-data/{}_tripdata_{}.parquet".format(
            i, value_taxi
        )
        output_file = "/mnt/shared/dfm/quarantine/{}/{}.parquet".format(i,value_taxi)
        response = requests.get(url)
        with open(output_file, "wb") as file:
            file.write(response.content)
        upload_to_s3(bucket_name, "{}/{}.parquet".format(i,value_taxi), output_file, access_key_id, secret_access_key)

def udpate_date_postgres(**context):
    # Connect to PostgreSQL using PostgresHook
    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    ##get the data from the postgres table
    sql_query = """UPDATE nyc
                   SET lastmonthprocessed  = date(lastmonthprocessed  + INTERVAL '1 month')"""

    result = postgres_hook.run(sql_query)

with DAG(
    "get_nyc_taxi_data",
    start_date=datetime(2023, 3, 14),
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:

    pull_month_to_be_processed = PythonOperator(
        task_id="pull_month_to_be_processed",
        python_callable=get_data_postgres,
        provide_context=True,
    )

    copy_data_to_s3 = PythonOperator(
        task_id="copy_data_to_s3",
        python_callable=download_data_nyc,
        provide_context=True,
    )
    update_next_month_date_postgres = PythonOperator(
        task_id="update_next_month_date_postgres",
        python_callable=udpate_date_postgres,
        provide_context=True,
    )
    cleanup_xcom_task = PythonOperator(
    task_id="cleanup_xcom",
    python_callable=cleanup_xcom,
    dag=dag
    )
    pull_month_to_be_processed >> copy_data_to_s3 >> update_next_month_date_postgres >> cleanup_xcom_task
