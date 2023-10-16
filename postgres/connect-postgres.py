
import psycopg2

# Establish connection
conn = psycopg2.connect(
    host="10.10.162.202",
    port="5432",
    database="postgres",
    user="postgres",
    password="postgres"
)
# Create a cursor
cursor = conn.cursor()
query="""SELECT taxitype, 
                CAST(EXTRACT(YEAR FROM new_date) as INTEGER) as year, LPAD(EXTRACT(MONTH FROM new_date)::text, 2, '0') as month
                FROM (SELECT  *, DATE((DATE_TRUNC('month', lastmonthprocessed) + INTERVAL '1 month')) AS new_date from nyc) as t
                """
# Execute a query
cursor.execute(query)

# Fetch and print the results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
