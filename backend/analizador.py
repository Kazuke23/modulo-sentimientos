# backend/analizador.py
from pysentimiento import create_analyzer

analyzer = create_analyzer(task="sentiment", lang="es")

def analizar_sentimientos(comentarios: list) -> list:
    resultado = []
    for c in comentarios:
        texto = c.get("texto_limpio", "")
        if texto:
            prediccion = analyzer.predict(texto)
            sentimiento = prediccion.output  # POS, NEG o NEU
            probabilidades = {
                "positivo": round(prediccion.probas.get("POS", 0), 3),
                "negativo": round(prediccion.probas.get("NEG", 0), 3),
                "neutro":   round(prediccion.probas.get("NEU", 0), 3),
            }
        else:
            sentimiento = "NEU"
            probabilidades = {"positivo": 0, "negativo": 0, "neutro": 1}

        resultado.append({**c, "sentimiento": sentimiento, "probabilidades": probabilidades})

    return resultado