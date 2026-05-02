import pandas as pd


def ler_excel(file_path):
    df = pd.read_excel(file_path, header=None)

    transacoes = []

    for i in range(len(df)):
        linha = df.iloc[i]

        try:
            data = str(linha[0]).strip()
            descricao = str(linha[1]).strip()
            valor = linha[2]

            # valida se é linha válida
            if data == "nan" or descricao == "nan":
                continue

            if isinstance(valor, str):
                valor = valor.replace(",", ".").replace("R$", "").strip()

            valor = float(valor)

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
