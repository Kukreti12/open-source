## read file from amazon s3

from pyspark.sql import SparkSession
import logging

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Connect to Amazon S3") \
    .config("spark.hadoop.fs.s3a.access.key", "") \
    .config("spark.hadoop.fs.s3a.secret.key", "") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "true") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.region", "us-east-1") \
    .getOrCreate()

    
# Set the log level for the Spark application
spark.sparkContext.setLogLevel("INFO")
df = spark.read.csv("s3a://ingestion-sprint7/sampleSubmission.csv")