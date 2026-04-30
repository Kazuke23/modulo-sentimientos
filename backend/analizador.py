import requests
import os

API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-xlm-roberta-base-sentiment"

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

            # 🔴 ERROR HTTP (como el 404 que tienes)
            if response.status_code != 200:
                print(f"HF STATUS ERROR ({response.status_code}):", response.text)

                resultado.append({
                    **c,
                    "sentimiento": "ERROR",
                    "probabilidades": {"positivo": 0, "negativo": 0, "neutro": 0}
                })
                continue

            data = response.json()

            # 🔴 ERROR DE HF (modelo cargando o fallo)
            if isinstance(data, dict):
                if "error" in data:
                    print("HF ERROR:", data)

                    resultado.append({
                        **c,
                        "sentimiento": "ERROR",
                        "probabilidades": {"positivo": 0, "negativo": 0, "neutro": 0}
                    })
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
                    label = item["label"]
                    score = round(item["score"], 3)

                    if label == "POS":
                        probabilidades["positivo"] = score
                    elif label == "NEG":
                        probabilidades["negativo"] = score
                    elif label == "NEU":
                        probabilidades["neutro"] = score

            else:
                print("Respuesta inesperada HF:", data)

                resultado.append({
                    **c,
                    "sentimiento": "ERROR",
                    "probabilidades": {"positivo": 0, "negativo": 0, "neutro": 0}
                })
                continue

        except Exception as e:
            print("ERROR ANALISIS:", e)

            resultado.append({
                **c,
                "sentimiento": "ERROR",
                "probabilidades": {"positivo": 0, "negativo": 0, "neutro": 0}
            })
            continue

        resultado.append({
            **c,
            "sentimiento": max_label,
            "probabilidades": probabilidades
        })

    return resultado