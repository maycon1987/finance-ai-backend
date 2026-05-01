import pdfplumber


def extrair_texto_pdf(file_path: str) -> str:
    texto = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            texto += page_text + "\n"

    return texto
