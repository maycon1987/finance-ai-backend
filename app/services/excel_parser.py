import pandas as pd


def ler_excel(file_path):
    df = pd.read_excel(file_path)

    df.columns = [c.lower() for c in df.columns]

    transacoes = []

    for _, row in df.iterrows():
        try:
            data = str(row.get("data", ""))
            descricao = str(row.get("histórico", row.get("descricao", "")))
            valor = float(row.get("valor", 0))

            tipo = "entrada" if valor > 0 else "saida"

            transacoes.append({
                "data": data,
                "descricao": descricao,
                "valor": valor,
                "tipo": tipo,
                "categoria": "Outros"
            })
        except:
            continue

    return transacoes
