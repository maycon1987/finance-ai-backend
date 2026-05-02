from fastapi import APIRouter, UploadFile, File
import os

from app.services.parser import extrair_texto_pdf
from app.services.organizer import extrair_transacoes
from app.services.ai_parser import extrair_com_ia
from app.services.ai_cleaner import limpar_json_ia
from app.services.excel_parser import ler_excel

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "storage"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/extrato")
async def upload_extrato(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 👉 SE FOR EXCEL
    if file.filename.endswith(".xlsx"):
        transacoes_final = ler_excel(file_path)

    else:
        texto = extrair_texto_pdf(file_path)

        transacoes_parser = extrair_transacoes(texto)

        resposta_ia = extrair_com_ia(texto)
        transacoes_ia = limpar_json_ia(resposta_ia)

        if isinstance(transacoes_ia, list) and len(transacoes_ia) > 0:
            transacoes_final = transacoes_ia
        else:
            transacoes_final = transacoes_parser

    total_entradas = sum(t["valor"] for t in transacoes_final if t["tipo"] == "entrada")
    total_saidas = sum(t["valor"] for t in transacoes_final if t["tipo"] == "saida")
    saldo = total_entradas + total_saidas

    return {
        "status": "ok",
        "filename": file.filename,
        "total_transacoes": len(transacoes_final),
        "total_entradas": round(total_entradas, 2),
        "total_saidas": round(total_saidas, 2),
        "saldo": round(saldo, 2),
        "transacoes": transacoes_final[:100]
    }
