from fastapi import APIRouter, UploadFile, File
import os

from app.services.parser import extrair_texto_pdf
from app.services.organizer import extrair_transacoes
from app.services.ai_parser import extrair_com_ia
from app.services.ai_cleaner import limpar_json_ia
from app.services.excel_parser import ler_excel
from app.services.excel_generator import gerar_excel

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "storage"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/extrato")
async def upload_extrato(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # salvar arquivo
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # =========================
    # SE FOR EXCEL
    # =========================
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

    # =========================
    # CALCULOS
    # =========================
    total_entradas = sum(t["valor"] for t in transacoes_final if t["valor"] > 0)
    total_saidas = sum(abs(t["valor"]) for t in transacoes_final if t["valor"] < 0)
    saldo = total_entradas - total_saidas

    # =========================
    # GERAR EXCEL
    # =========================
    nome_limpo = file.filename.replace(".xlsx", "").replace(".pdf", "")
output_path = f"{UPLOAD_DIR}/resultado_{nome_limpo}.xlsx"
    gerar_excel(transacoes_final, output_path)

    # =========================
    # RETORNO
    # =========================
    return {
        "status": "ok",
        "filename": file.filename,
        "total_transacoes": len(transacoes_final),
        "total_entradas": round(total_entradas, 2),
        "total_saidas": round(total_saidas, 2),
        "saldo": round(saldo, 2),
        "excel_gerado": output_path,
        "transacoes": transacoes_final[:50]
    }
