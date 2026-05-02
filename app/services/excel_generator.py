import pandas as pd
from collections import defaultdict
from datetime import datetime


def gerar_excel(transacoes, file_path_saida):
    df = pd.DataFrame(transacoes)

    if df.empty:
        return None

    # =========================
    # NORMALIZAÇÃO
    # =========================
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)

    df["entrada"] = df["valor"].apply(lambda x: x if x > 0 else 0)
    df["saida"] = df["valor"].apply(lambda x: abs(x) if x < 0 else 0)

    # =========================
    # RESUMO GERAL
    # =========================
    total_entradas = df["entrada"].sum()
    total_saidas = df["saida"].sum()
    saldo = total_entradas - total_saidas

    resumo_df = pd.DataFrame([
        {"Tipo": "Total Entradas", "Valor": total_entradas},
        {"Tipo": "Total Saídas", "Valor": total_saidas},
        {"Tipo": "Saldo", "Valor": saldo},
    ])

    # =========================
    # POR CATEGORIA
    # =========================
    categoria_df = df.groupby("categoria")["valor"].sum().reset_index()
    categoria_df = categoria_df.sort_values(by="valor", ascending=False)

    # =========================
    # POR DIA
    # =========================
    try:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        diario_df = df.groupby(df["data"].dt.date)["valor"].sum().reset_index()
    except:
        diario_df = pd.DataFrame()

    # =========================
    # EXPORTAÇÃO
    # =========================
    with pd.ExcelWriter(file_path_saida, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Transacoes", index=False)
        resumo_df.to_excel(writer, sheet_name="Resumo", index=False)
        categoria_df.to_excel(writer, sheet_name="Por Categoria", index=False)

        if not diario_df.empty:
            diario_df.to_excel(writer, sheet_name="Por Dia", index=False)

    return file_path_saida
