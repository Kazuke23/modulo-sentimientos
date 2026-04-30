import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/pysentimiento/robertuito-sentiment-analysis"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}

def analizar_sentimientos(comentarios: list) -> list:
    resultado = []

    for c in comentarios:
        texto = c.get("texto_limpio", "")

        if texto:
            try:
                response = requests.post(
                    API_URL,
                    headers=HEADERS,
                    json={
                        "inputs": texto,
                        "parameters": {
                            "return_all_scores": True
                        }
                    }
                )

                data = response.json()

                # Ejemplo esperado:
                # [[
                #   {"label": "NEG", "score": 0.1},
                #   {"label": "NEU", "score": 0.2},
                #   {"label": "POS", "score": 0.7}
                # ]]

                if isinstance(data, list) and len(data) > 0:
                    scores = data[0]

                    probabilidades = {
                        "positivo": 0,
                        "negativo": 0,
                        "neutro": 0
                    }

                    max_label = "NEU"
                    max_score = 0

                    for item in scores:
                        label = item["label"]
                        score = round(item["score"], 3)

                        if label == "POS":
                            probabilidades["positivo"] = score
                        elif label == "NEG":
                            probabilidades["negativo"] = score
                        elif label == "NEU":
                            probabilidades["neutro"] = score

                        if score > max_score:
                            max_score = score
                            max_label = label

                else:
                    max_label = "NEU"
                    probabilidades = {"positivo": 0, "negativo": 0, "neutro": 1}

            except Exception as e:
                print("Error:", e)
                max_label = "NEU"
                probabilidades = {"positivo": 0, "negativo": 0, "neutro": 1}

        else:
            max_label = "NEU"
            probabilidades = {"positivo": 0, "negativo": 0, "neutro": 1}

        resultado.append({
            **c,
            "sentimiento": max_label,
            "probabilidades": probabilidades
        })

    return resultado