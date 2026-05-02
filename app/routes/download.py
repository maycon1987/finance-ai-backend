from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/download", tags=["Download"])

UPLOAD_DIR = "storage"


@router.get("/{filename}")
def download_excel(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        return {
            "erro": "Arquivo não encontrado",
            "procurando_em": file_path
        }

    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )
