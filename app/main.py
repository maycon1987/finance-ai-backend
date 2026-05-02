from fastapi import FastAPI

from app.routes import upload
from app.routes import download

app = FastAPI(title="Finance AI API")


app.include_router(upload.router)
app.include_router(download.router)


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
