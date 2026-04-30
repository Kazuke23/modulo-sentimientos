import requests
import os

API_URL = "https://api-inference.huggingface.co/models/pysentimiento/robertuito-sentiment-analysis"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
}

def analizar_sentimientos(comentarios: list) -> list:
    resultado = []

    for c in comentarios:
        texto = c.get("texto_original", "")

        if not texto:
            continue

        try:
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json={
                    "inputs": texto,
                    "options": {"wait_for_model": True}
                },
                timeout=20
            )

            # 🔴 ERROR HTTP
            if response.status_code != 200:
                print("HF ERROR STATUS:", response.status_code, response.text)
                continue

            data = response.json()

            # 🔴 ERROR DE HF
            if isinstance(data, dict) and "error" in data:
                print("HF ERROR:", data)
                continue

            # ✅ RESPUESTA NORMAL
            if isinstance(data, list) and len(data) > 0:
                scores = data[0]

                max_item = max(scores, key=lambda x: x["score"])
                max_label = max_item["label"]

                probabilidades = {
                    "positivo": 0,
                    "negativo": 0,
                    "neutro": 0
                }

                for item in scores:
                    if item["label"] == "POS":
                        probabilidades["positivo"] = round(item["score"], 3)
                    elif item["label"] == "NEG":
                        probabilidades["negativo"] = round(item["score"], 3)
                    elif item["label"] == "NEU":
                        probabilidades["neutro"] = round(item["score"], 3)

                resultado.append({
                    **c,
                    "sentimiento": max_label,
                    "probabilidades": probabilidades
                })

        except Exception as e:
            print("ERROR ANALISIS:", e)
            continue

    return resultado