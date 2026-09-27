import os
from fastapi import FastAPI, HTTPException, Request
import psycopg2

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")


@app.get("/")
def health():
    return {"status": "healthy"}


@app.get("/db-check")
def db_check():
    if not DATABASE_URL:
        raise HTTPException(status_code=500, detail="DATABASE_URL not set")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        try:
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()
            cur.close()
            return {"db_version": version[0]}
        finally:
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB connection failed: {e}")


@app.get("/debug/request-info")
def request_info(request: Request):
    """inspect the request object and return some useful information for debugging"""
    return {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "path_params": request.path_params,
        "query_params": dict(request.query_params),
    }
