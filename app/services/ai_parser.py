import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extrair_com_ia(texto):
    prompt = f"""
Você é um especialista em leitura de extratos bancários brasileiros.

Converta o texto abaixo em uma lista JSON de transações.

Regras:
- Cada transação deve ter:
  - data (DD/MM)
  - descricao
  - valor (negativo para saída)
  - tipo (entrada ou saida)
- Valores com "C" são entrada
- Valores com "D" são saída
- Ignore linhas como DOC, CPF, CNPJ isolados
- Junte linhas quebradas

Texto:
{texto[:8000]}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Você extrai dados financeiros com precisão."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
