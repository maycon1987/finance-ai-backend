from fastapi import FastAPI

app = FastAPI(title="Finance AI API")

@app.get("/")
def home():
    return {
        "status": "online",
        "app": "Finance AI API"
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
