from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/download", tags=["Download"])

@router.get("/")
def download_excel(path: str):
    if not os.path.exists(path):
        return {"erro": "Arquivo não encontrado"}

    return FileResponse(
        path,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename=os.path.basename(path)
    )
