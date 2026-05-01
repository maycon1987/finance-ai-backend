import json
import re


def limpar_json_ia(resposta_ia: str):
    try:
        resposta_ia = re.sub(r"```json", "", resposta_ia)
        resposta_ia = re.sub(r"```", "", resposta_ia)
        resposta_ia = resposta_ia.strip()

        return json.loads(resposta_ia)

    except Exception as e:
        return {
            "erro": str(e),
            "raw": resposta_ia
        }
