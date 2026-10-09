import os
import logging
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import psycopg2
from dotenv import load_dotenv
from typing import Optional

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    conversation_id: Optional[str] = None

conversations = {}

def get_or_create_conversation(conversation_id=None):
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    return conversation_id

def get_conversation_history(conversation_id):
    return conversations.get(conversation_id, [])

def save_message(conversation_id, role, content):
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    conversations[conversation_id].append({"role": role, "content": content})


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
            if version:
                return {"db_version": version[0]}
            else:
                raise HTTPException(status_code=500, detail="No database version returned")
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
        logger.error(f"Ollama call failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Ollama call failed: {e}")


@app.post("/ask", summary="Ask Ollama a question via POST",
          description="Send a question with full conversation context",
          response_description="Question and answer from Ollama model with conversation ID")
def ask_ollama_post(question: Question):
    """Send a question with full conversation history maintained"""
    if not ollama_client:
        raise HTTPException(status_code=500, detail="Ollama client not configured. Set BASE_URL and API_KEY")

    model_to_use = question.model or MODEL
    if not model_to_use:
        raise HTTPException(status_code=500, detail="MODEL environment variable not set")

    try:
        logger.info(f"POST /ask received: text={question.text}, conversation_id={question.conversation_id}")
        conversation_id = get_or_create_conversation(question.conversation_id)
        logger.info(f"After get_or_create: conversation_id={conversation_id}")
        history = get_conversation_history(conversation_id)
        messages = history + [{"role": "user", "content": question.text}]

        response = ollama_client.chat.completions.create(
            model=model_to_use,
            messages=messages
        )

        answer = response.choices[0].message.content
        save_message(conversation_id, "user", question.text)
        save_message(conversation_id, "assistant", answer)

        return {
            "conversation_id": conversation_id,
            "question": question.text,
            "model": model_to_use,
            "answer": answer,
            "history_length": len(history)
        }
    except Exception as e:
        logger.error(f"Ollama call failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Ollama call failed: {e}")


@app.get("/conversation/{conversation_id}", summary="Get conversation history",
         description="Retrieve all messages in a conversation")
def get_conversation(conversation_id: str):
    """Get full conversation history"""
    messages = get_conversation_history(conversation_id)
    return {
        "conversation_id": conversation_id,
        "messages": messages,
        "message_count": len(messages)
    }


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
