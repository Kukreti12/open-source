"""
Demo script for reading a CSV file from S3 into a pandas data frame using the boto3 library
"""

import os

import boto3
import pandas as pd


AWS_S3_BUCKET = "aws-glue-bi-test"
AWS_ACCESS_KEY_ID = "***"
AWS_SECRET_ACCESS_KEY = "***"


s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

response = s3_client.get_object(
    Bucket=AWS_S3_BUCKET,
    Key="demo/release/data/etl-data/transaction/process_date=2021-05-07/part-00000-93f5a6a0-2ca6-4ebe-aca0-1b327c6ba142-c000.snappy.parquet",
)

status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

if status == 200:
    print(f"Successful S3 get_object response. Status - {status}")
    df = pd.read_parquet(response.get("Body"))
    print(df.shape)
else:
    print(f"Unsuccessful S3 get_object response. Status - {status}")
