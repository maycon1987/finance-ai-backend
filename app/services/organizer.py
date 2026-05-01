import re


def limpar_valor(valor_str: str) -> float:
    valor = valor_str.replace(" ", "")
    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")
    return float(valor)


def definir_tipo(descricao: str) -> str:
    descricao_upper = descricao.upper()

    palavras_entrada = [
        "RECEBIDO",
        "CREDITO",
        "CRÉDITO",
        "DEPOSITO",
        "DEPÓSITO",
        "TRANSFERENCIA RECEBIDA",
        "PIX RECEBIDO",
        "TED RECEBIDA",
        "DOC RECEBIDO",
        "CARTÃO",
        "CARTAO",
    ]

    for palavra in palavras_entrada:
        if palavra in descricao_upper:
            return "entrada"

    return "saida"


def extrair_transacoes(texto: str):
    linhas = texto.split("\n")
    transacoes = []

    for linha in linhas:
        match = re.search(
            r"(\d{2}/\d{2}/\d{4})\s+(.*?)\s+R\$\s*([\d\.,\s]+)",
            linha
        )

        if match:
            data = match.group(1)
            descricao = match.group(2).strip()
            valor_str = match.group(3)

            try:
                valor = limpar_valor(valor_str)
            except Exception:
                continue

            tipo = definir_tipo(descricao)

            if tipo == "saida":
                valor = -abs(valor)
            else:
                valor = abs(valor)

            transacoes.append({
                "data": data,
                "descricao": descricao,
                "valor": valor,
                "tipo": tipo
            })

    return transacoes
