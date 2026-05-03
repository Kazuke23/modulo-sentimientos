# backend/analizador.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/lxyuan/distilbert-base-multilingual-cased-sentiments-student/pipeline/text-classification"

def analizar_sentimientos(comentarios: list) -> list:
    token = os.getenv("HF_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    resultado = []

    for c in comentarios:
        texto = c.get("texto_limpio", c.get("texto_original", ""))

        if not texto:
            continue

        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json={"inputs": texto[:512]},
                timeout=30
            )

            if response.status_code != 200:
                print(f"HF STATUS ERROR ({response.status_code}):", response.text)
                sentimiento = "NEU"
                probabilidades = {"positivo": 0.0, "negativo": 0.0, "neutro": 1.0}
            else:
                data = response.json()

                if isinstance(data, dict) and "error" in data:
                    print("HF MODEL ERROR:", data["error"])
                    sentimiento = "NEU"
                    probabilidades = {"positivo": 0.0, "negativo": 0.0, "neutro": 1.0}
                else:
                    # El modelo retorna lista de listas o lista de dicts
                    scores = data[0] if isinstance(data[0], list) else data

                    label_map = {
                        "positive": "POS",
                        "negative": "NEG",
                        "neutral":  "NEU"
                    }
                    prob_map = {
                        "positive": "positivo",
                        "negative": "negativo",
                        "neutral":  "neutro"
                    }

                    probabilidades = {"positivo": 0.0, "negativo": 0.0, "neutro": 0.0}
                    best_label = "NEU"
                    best_score = 0.0

                    for item in scores:
                        label = item["label"].lower()
                        score = round(item["score"], 3)

                        if label in prob_map:
                            probabilidades[prob_map[label]] = score

                        if score > best_score:
                            best_score = score
                            best_label = label_map.get(label, "NEU")

                    sentimiento = best_label

        except Exception as e:
            print("ERROR ANALISIS:", e)
            sentimiento = "NEU"
            probabilidades = {"positivo": 0.0, "negativo": 0.0, "neutro": 1.0}

        resultado.append({
            **c,
            "sentimiento": sentimiento,
            "probabilidades": probabilidades
        })

    return resultado