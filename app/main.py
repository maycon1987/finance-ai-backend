from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import upload
from app.routes import download

app = FastAPI(title="Finance AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
