from fastapi import APIRouter, UploadFile, File
import os
from app.services.parser import extrair_texto_pdf

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "storage"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/extrato")
async def upload_extrato(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    texto = extrair_texto_pdf(file_path)

    return {
        "status": "ok",
        "filename": file.filename,
        "preview_texto": texto[:1000]  # só primeiros 1000 caracteres
    }
