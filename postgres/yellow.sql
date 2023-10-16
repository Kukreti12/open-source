CREATE TABLE IF NOT EXISTS yellow(
VendorID bigint ,
tpep_pickup_datetime timestamp ,
tpep_dropoff_datetime timestamp ,
passenger_count double precision ,
trip_distance double precision ,
RatecodeID double precision ,
store_and_fwd_flag varchar(255) ,
PULocationID bigint ,
DOLocationID bigint ,
payment_type bigint ,
fare_amount double precision ,
extra double precision ,
mta_tax double precision, 
tip_amount double precision ,
tolls_amount double precision, 
improvement_surcharge double precision ,
total_amount double precision ,
congestion_surcharge double precision ,
airport_fee double precision 
);