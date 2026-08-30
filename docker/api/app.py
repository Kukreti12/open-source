import os
from fastapi import FastAPI
import psycopg2

app = FastAPI()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@host.docker.internal:5432/mydb"
)

@app.get("/")
def health():
    return {"status": "healthy"}

@app.get("/db-check")
def db_check():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    cur.close()
    conn.close()
    return {"db_version": version}