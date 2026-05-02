from app.routes import download
app.include_router(download.router)
from fastapi import FastAPI
from app.routes import upload

app = FastAPI(title="Finance AI API")

app.include_router(upload.router)

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
