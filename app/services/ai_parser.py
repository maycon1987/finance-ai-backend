import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def dividir_texto(texto, tamanho=6000):
    return [texto[i:i + tamanho] for i in range(0, len(texto), tamanho)]


def extrair_com_ia(texto: str):
    try:
        partes = dividir_texto(texto)
        resultados = []

        for parte in partes:
            prompt = f"""
Você é um especialista em leitura de extratos bancários brasileiros.

Converta o texto abaixo em JSON estruturado.

Regras:
- Cada transação deve ter:
  - data (DD/MM)
  - descricao
  - valor (negativo para saída)
  - tipo (entrada ou saida)
  - categoria
- Valores com "C" são entrada
- Valores com "D" são saída
- Junte linhas quebradas
- Ignore lixo como CPF, DOC isolado

Texto:
{parte}
"""

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Você extrai dados financeiros com precisão."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            resultados.append(response.choices[0].message.content)

        return "\n".join(resultados)

    except Exception as e:
        return f"erro_ia: {str(e)}"
