import re
import pandas as pd
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


COR_ROXO = "5B2C83"
COR_AMARELO = "FFD966"
COR_VERDE = "D9EAD3"
COR_CINZA = "F2F2F2"
COR_BRANCO = "FFFFFF"


def moeda(valor):
    try:
        return float(valor)
    except Exception:
        return 0.0


def limpar_nome_cliente(detalhes):
    if not detalhes:
        return ""

    partes = [p.strip() for p in str(detalhes).split("|") if p.strip()]

    remover = [
        "Recebimento Pix",
        "Pagamento Pix",
        "Transferência Pix",
        "MHM CAIXAS COMERCIO DE EMBALAGENS LTDA",
    ]

    candidatos = []

    for p in partes:
        if any(r.upper() in p.upper() for r in remover):
            continue
        if re.search(r"\d{2}\.\d{3}\.\d{3}", p):
            continue
        if "***" in p:
            continue
        candidatos.append(p)

    return candidatos[0] if candidatos else ""


def limpar_nome_fornecedor(texto):
    if not texto:
        return "Sem Fornecedor"

    t = str(texto).upper().strip()

    t = t.replace("FORNECEDOR", "")
    t = t.replace("FAV.:", "")
    t = t.replace("FAV:", "")

    t = re.sub(r"\bNF\b.*", "", t)
    t = re.sub(r"\bNFE\b.*", "", t)
    t = re.sub(r"\bNOTA\b.*", "", t)
    t = re.sub(r"\bRM\b.*", "", t)
    t = re.sub(r"\bRMS\b.*", "", t)
    t = re.sub(r"\bREF\b.*", "", t)
    t = re.sub(r"\bPEDIDO\b.*", "", t)
    t = re.sub(r"\bBOLETO\b.*", "", t)

    t = re.sub(r"\d+", "", t)
    t = re.sub(r"[-–—_/]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()

    regras = {
        "CYCLOPACK": "Cyclopack",
        "TECNIPACK": "Tecnipack",
        "TECHNIPACK": "Tecnipack",
        "NOVAPLASTIC": "Novaplastic",
        "NOVABOLHA": "Novabolha",
        "WEBPACK": "F Webpack",
        "F WEBPACK": "F Webpack",
        "UNIPEL": "Unipel",
        "ITA CHINESA": "Fita Chinesa",
        "FITACHINESA": "Fita Chinesa",
        "HF AMBIENT
