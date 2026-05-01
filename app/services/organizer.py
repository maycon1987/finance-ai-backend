import re

def extrair_transacoes(texto):
    linhas = texto.split("\n")
    transacoes = []

    for linha in linhas:
        match = re.search(r'(\d{2}/\d{2}/\d{4})\s+(.*?)\s+R\$\s*([\d\.,\s]+)', linha)

        if match:
            data = match.group(1)
            descricao = match.group(2).strip()
            valor_str = match.group(3)

            # limpar valor
            valor = valor_str.replace(" ", "").replace(".", "").replace(",", ".")
            valor = float(valor)

            # definir tipo
            if "RECEBIDO" in descricao:
                tipo = "entrada"
            else:
                tipo = "saida"
                valor = -valor

            transacoes.append({
                "data": data,
                "descricao": descricao,
                "valor": valor,
                "tipo": tipo
            })

    return transacoes
