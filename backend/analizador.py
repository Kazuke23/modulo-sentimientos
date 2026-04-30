import requests
import os

API_URL = "https://api-inference.huggingface.co/models/pysentimiento/robertuito-sentiment-analysis"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}

def analizar_sentimientos(comentarios: list) -> list:
    resultado = []

    for c in comentarios:
        # 🔥 usamos texto_original para no perder info
        texto = c.get("texto_original", "")

        if not texto:
            continue

        try:
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json={
                    "inputs": texto,
                    "parameters": {"return_all_scores": True}
                },
                timeout=10
            )

            data = response.json()

            # 🔴 VALIDAR ERROR DE HF
            if isinstance(data, dict) and "error" in data:
                print("HF ERROR:", data)
                continue

            if isinstance(data, list) and len(data) > 0:
                scores = data[0]

                # 🔥 tomar el mayor directamente
                max_item = max(scores, key=lambda x: x["score"])
                max_label = max_item["label"]

                probabilidades = {
                    "positivo": 0,
                    "negativo": 0,
                    "neutro": 0
                }

                for item in scores:
                    label = item["label"]
                    score = round(item["score"], 3)

                    if label == "POS":
                        probabilidades["positivo"] = score
                    elif label == "NEG":
                        probabilidades["negativo"] = score
                    elif label == "NEU":
                        probabilidades["neutro"] = score

            else:
                print("Respuesta rara HF:", data)
                continue

        except Exception as e:
            print("ERROR ANALISIS:", e)
            continue

        resultado.append({
            **c,
            "sentimiento": max_label,
            "probabilidades": probabilidades
        })

    return resultado