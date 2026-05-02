import re
import html
import pandas as pd


def limpar_celula(valor):
    if pd.isna(valor):
        return ""

    texto = str(valor)
    texto = html.unescape(texto)
    texto = texto.replace("\xa0", " ")
    texto = texto.strip()

    if texto in ["6", "6.0", "nan", "None"]:
        return ""

    return texto


def eh_data(texto):
    return bool(re.match(r"^\d{2}/\d{2}/\d{4}$", texto))


def converter_valor(valor_raw):
    texto = limpar_celula(valor_raw).upper()

    if not texto:
        return None

    if not ("C" in texto or "D" in texto):
        return None

    sinal = -1 if "D" in texto or "-" in texto else 1

    texto = texto.replace("R$", "")
    texto = texto.replace("C", "")
    texto = texto.replace("D", "")
    texto = texto.replace("*", "")
    texto = texto.replace("-", "")
    texto = texto.replace(" ", "")
    texto = texto.replace(".", "")
    texto = texto.replace(",", ".")

    try:
        return round(float(texto) * sinal, 2)
    except:
        return None


def categorizar(descricao, valor):
    d = descricao.upper()

    if "SALDO" in d:
        return "Ignorar"

    # ENTRADAS
    if valor > 0:
        if "PIX RECEB" in d:
            return "Receitas"
        if "CR" in d or "CRED" in d:
            return "Receitas"
        if "ANTECIPA" in d:
            return "Receitas"
        return "Receitas"

    # SAÍDAS
    if valor < 0:
        if "FORNECEDOR" in d or "DÉB.TIT" in d or "DEB.TIT" in d:
            return "Fornecedores"

        if "SALARIO" in d or "SALÁRIO" in d or "FERIAS" in d:
            return "Salários"

        if "LUCRO" in d:
            return "Distribuição de Lucros"

        if "IMPOSTO" in d or "DAS" in d:
            return "Impostos"

        if "TARIFA" in d or "PACOTE" in d:
            return "Taxas Bancárias"

        return "Despesas"

    return "Outros"


def ler_excel(file_path):
    df = pd.read_excel(file_path, header=None, dtype=object)

    transacoes = []
    transacao_atual = None

    for _, row in df.iterrows():
        data = limpar_celula(row.iloc[0]) if len(row) > 0 else ""
        documento = limpar_celula(row.iloc[1]) if len(row) > 1 else ""
        historico = limpar_celula(row.iloc[2]) if len(row) > 2 else ""
        valor_raw = limpar_celula(row.iloc[3]) if len(row) > 3 else ""

        # Nova transação começa quando a coluna A é uma data válida
        if eh_data(data):
            valor = converter_valor(valor_raw)

            if valor is None:
                continue

            if "SALDO" in historico.upper():
                continue

            transacao_atual = {
                "data": data,
                "documento": documento,
                "descricao": historico,
                "detalhes": "",
                "valor": valor,
                "tipo": "entrada" if valor > 0 else "saida",
                "categoria": categorizar(historico),
            }

            transacoes.append(transacao_atual)

        else:
            # Linhas abaixo da transação são detalhes
            if transacao_atual and historico:
                if transacao_atual["detalhes"]:
                    transacao_atual["detalhes"] += " | " + historico
                else:
                    transacao_atual["detalhes"] = historico

                descricao_completa = (
                    transacao_atual["descricao"] + " " + transacao_atual["detalhes"]
                )

                transacao_atual["categoria"] = categorizar(descricao_completa)

    return transacoes
