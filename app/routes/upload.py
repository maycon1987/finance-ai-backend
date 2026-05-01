from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "storage"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/extrato")
async def upload_extrato(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "status": "ok",
        "filename": file.filename,
        "file_path": file_path
    }
