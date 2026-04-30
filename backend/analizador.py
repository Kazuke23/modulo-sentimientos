import requests
import os
import time

API_URL = "https://api-inference.huggingface.co/models/pysentimiento/robertuito-sentiment-analysis"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}

def analizar_sentimientos(comentarios: list) -> list:
    resultado = []

    for c in comentarios:
        texto = c.get("texto_original", "")

        # 🔴 si no hay texto
        if not texto:
            resultado.append({
                **c,
                "sentimiento": "ERROR",
                "probabilidades": {"positivo": 0, "negativo": 0, "neutro": 0}
            })
            continue

        max_label = "ERROR"
        probabilidades = {"positivo": 0, "negativo": 0, "neutro": 0}

        # 🔁 retry automático (3 intentos)
        for intento in range(3):
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

                # 🚨 validar status HTTP
                if response.status_code != 200:
                    print(f"HF STATUS ERROR ({response.status_code}):", response.text)
                    time.sleep(2)
                    continue

                # 🚨 validar respuesta vacía
                if not response.text:
                    print("HF RESPUESTA VACÍA")
                    time.sleep(2)
                    continue

                # 🚨 parse seguro
                try:
                    data = response.json()
                except Exception:
                    print("ERROR PARSE JSON:", response.text)
                    time.sleep(2)
                    continue

                # 🚨 error de HF (modelo cargando, etc)
                if isinstance(data, dict) and "error" in data:
                    print("HF ERROR:", data)
                    time.sleep(2)
                    continue

                # ✅ respuesta válida
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

                    break  # 🔥 sale del retry si todo salió bien

                else:
                    print("HF RESPUESTA RARA:", data)
                    time.sleep(2)

            except Exception as e:
                print("ERROR REQUEST:", e)
                time.sleep(2)

        resultado.append({
            **c,
            "sentimiento": max_label,
            "probabilidades": probabilidades
        })

    return resultado