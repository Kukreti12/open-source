from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health():
    return {"status": "healthy"}

@app.post("/predict")
def predict(payload: dict):
    return {
        "request": payload,
        "response": "Hello from Dockerized Python API"
    }
