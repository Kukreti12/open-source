from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
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
    "retry_delay": timedelta(minutes=5)
}

def download_rates():
    # Specify the API endpoint URL
    url = 'https://api.wazirx.com/sapi/v1/tickers/24hr'
    # Make an HTTP GET request to the API
    response = requests.get(url)

    # Parse the response content as JSON and store it in a Python object
    data = response.json()
    df = pd.DataFrame(data)
    df.columns = map(str.lower, df.columns)
    csv_path = '/opt/airflow/dags/file.csv'
    df.to_csv(csv_path, index=False)
    ## Convert the json object to dataframe
    conn_string = 'postgresql://postgres:mysecretpassword@10.10.162.165:5432/postgres'
    db = create_engine(conn_string)
    conn = db.connect()
    df.to_sql('bitcoin', con=conn, if_exists='append',
          index=False)
    conn.close()


def s3_upload():
    s3_resource = boto3.resource('s3',
                        endpoint_url='https://mapr1.ailab.local:9000',
                        aws_access_key_id='R3N4IUCGKRQPU9KMQTTKK02DGYHIM9B3CWJBKS43CEO6X8TRXLQ3PRMC9KT305ZNH3H9BOC4LHJLQNDGWYOAUZORAT1OMTMCGZ06P042G4TZFX0OEO2RT3MT2XQQ',
                        aws_secret_access_key='B1LWRXF0INQKA3BENHU6V6H1A8X128ORQS9K0Z787ZZK1MB6JSCY2G4HTTZMPJL0PPB363A1R3RSN0MP5CTXSV56ARS6LPR53FPS0918O1YJ445',
                        verify= '/opt/airflow/dags/df.pem')

    # download the object 'your_file.gz' from the bucket 'your_bucket' and save it to local FS as your_file_downloaded.gz
    #s3.Bucket('your_bucket').download_file('your_directory/your_file.gz', 'your_file_downloaded.gz')
    s3_resource.Bucket("analyticsdata").upload_file('/opt/airflow/file.csv','bronze/file.csv')

with DAG("ingestion", start_date=datetime(2023, 3 ,14), 
    schedule_interval="@daily",
    default_args=default_args, catchup=False,) as dag:


    downloading_rates = PythonOperator(
            task_id="downloading_rates",
            python_callable=download_rates
    )

    
    s3_upload_task = PythonOperator(
            task_id="s3_upload",
            python_callable=s3_upload
    )

    # create_table = PostgresOperator(
    # task_id='create_table',
    # sql="/sql/bitcoin-ddl.sql"
    # )

    downloading_rates >> s3_upload_task