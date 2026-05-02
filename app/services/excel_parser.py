import pandas as pd


def ler_excel(file_path):
    df = pd.read_excel(file_path)

    # limpar nomes das colunas
    df.columns = [str(c).strip().lower() for c in df.columns]

    print("COLUNAS ENCONTRADAS:", df.columns)

    transacoes = []

    for _, row in df.iterrows():
        try:
            # tenta achar colunas automaticamente
            data = row.get("data") or row.get("data lançamento") or row.get("data lancamento")
            descricao = row.get("histórico") or row.get("historico") or row.get("descricao")
            valor = row.get("valor") or row.get("valor (r$)") or row.get("movimento")

            if pd.isna(valor):
                continue

            valor = float(valor)

            tipo = "entrada" if valor > 0 else "saida"

            transacoes.append({
                "data": str(data),
                "descricao": str(descricao),
                "valor": valor,
                "tipo": tipo,
                "categoria": "Outros"
            })

        except:
            continue

    return transacoes
