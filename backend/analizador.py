import requests
import os

API_URL = "https://api-inference.huggingface.co/models/pysentimiento/robertuito-sentiment-analysis"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    "Content-Type": "application/json"
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
                json={"inputs": texto},
                timeout=15
            )

            # ❌ Error HTTP
            if response.status_code != 200:
                print(f"HF STATUS ERROR ({response.status_code}):", response.text)
                continue

            data = response.json()

            # ❌ Error de HF (modelo cargando o fallo)
            if isinstance(data, dict) and "error" in data:
                print("HF ERROR:", data)
                continue

            # ✅ Respuesta correcta
            if isinstance(data, list) and len(data) > 0:
                scores = data[0]

                # 🔥 Tomar el score más alto
                max_item = max(scores, key=lambda x: x["score"])
                label = max_item["label"]  # ej: "1 star", "5 stars"

                # 🔥 Convertir estrellas → sentimiento
                if "1" in label or "2" in label:
                    max_label = "NEG"
                elif "3" in label:
                    max_label = "NEU"
                else:
                    max_label = "POS"

                # 🔥 Probabilidades agrupadas
                probabilidades = {
                    "positivo": 0,
                    "negativo": 0,
                    "neutro": 0
                }

                for item in scores:
                    lbl = item["label"]
                    score = round(item["score"], 3)

                    if "1" in lbl or "2" in lbl:
                        probabilidades["negativo"] += score
                    elif "3" in lbl:
                        probabilidades["neutro"] += score
                    else:
                        probabilidades["positivo"] += score

            else:
                print("Respuesta inesperada HF:", data)
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