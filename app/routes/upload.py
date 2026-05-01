from app.services.ai_cleaner import limpar_json_ia
from fastapi import APIRouter, UploadFile, File
import os

from app.services.parser import extrair_texto_pdf
from app.services.organizer import extrair_transacoes
from app.services.ai_parser import extrair_com_ia

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "storage"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/extrato")
async def upload_extrato(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    texto = extrair_texto_pdf(file_path)

    # Parser simples
    transacoes = extrair_transacoes(texto)

    total_entradas = sum(t["valor"] for t in transacoes if t["tipo"] == "entrada")
    total_saidas = sum(t["valor"] for t in transacoes if t["tipo"] == "saida")
    saldo = total_entradas + total_saidas

    # IA para extratos mais crus/bagunçados
   resposta_ia = extrair_com_ia(texto)
transacoes_ia = limpar_json_ia(resposta_ia)

    return {
    "status": "ok",
    "filename": file.filename,

    "parser_simples": {
        "total_transacoes": len(transacoes),
        "total_entradas": round(total_entradas, 2),
        "total_saidas": round(total_saidas, 2),
        "saldo": round(saldo, 2),
        "transacoes": transacoes[:50],
    },

    "ia": {
        "total_transacoes": len(transacoes_ia) if isinstance(transacoes_ia, list) else 0,
        "transacoes": transacoes_ia[:50] if isinstance(transacoes_ia, list) else transacoes_ia
    }
}
