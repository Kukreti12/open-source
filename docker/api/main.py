import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")

app = FastAPI(
    title="Dockerized Python API",
    description="A simple API built with FastAPI and Docker",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Ollama client if BASE_URL is provided
if BASE_URL and API_KEY:
    ollama_client = OpenAI(
        base_url=BASE_URL,
        api_key=API_KEY
    )
else:
    ollama_client = None


class Question(BaseModel):
    text: str
    model: str = 'qwen:4b'


@app.get("/")
def health():
    return {"status": "healthy", "api": "running"}


@app.get("/health")
def health_check():
    return {"status": "ok", "ollama_configured": ollama_client is not None}


@app.get("/db-check", summary="Check database connection",
         description="Checks if the application can connect to the database and returns the database version.",
         response_description="Database version if connection is successful.")
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


@app.get("/ask", summary="Ask Ollama a question",
         description="Send a question to Ollama and get a response",
         response_description="Question and answer from Ollama model")
def ask_ollama(question: str = "What is Artificial Intelligence?"):
    """Send a question to Ollama and get a response"""
    if not ollama_client:
        raise HTTPException(status_code=500, detail="Ollama client not configured. Set BASE_URL and API_KEY")

    if not MODEL:
        raise HTTPException(status_code=500, detail="MODEL environment variable not set")

    try:
        response = ollama_client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return {
            "question": question,
            "model": MODEL,
            "answer": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama call failed: {e}")


@app.post("/ask", summary="Ask Ollama a question via POST",
          description="Send a longer question to Ollama via POST request",
          response_description="Question and answer from Ollama model")
def ask_ollama_post(question: Question):
    """Send a question to Ollama via POST (for longer questions)"""
    if not ollama_client:
        raise HTTPException(status_code=500, detail="Ollama client not configured. Set BASE_URL and API_KEY")

    model_to_use = question.model or MODEL
    if not model_to_use:
        raise HTTPException(status_code=500, detail="MODEL environment variable not set")

    try:
        response = ollama_client.chat.completions.create(
            model=model_to_use,
            messages=[
                {
                    "role": "user",
                    "content": question.text
                }
            ]
        )
        return {
            "question": question.text,
            "model": model_to_use,
            "answer": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama call failed: {e}")


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
