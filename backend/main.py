from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.scraper import extraer_comentarios
from backend.preprocesador import preprocesar_comentarios
from backend.analizador import analizar_sentimientos

app = FastAPI(title="API Análisis Semántico")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SolicitudAnalisis(BaseModel):
    url: str
    max_comentarios: int = 100

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando correctamente"}

@app.post("/analizar")
def analizar(solicitud: SolicitudAnalisis):
    if not solicitud.url:
        raise HTTPException(status_code=400, detail="URL requerida")

    try:
        comentarios = extraer_comentarios(
            solicitud.url,
            solicitud.max_comentarios
        )

        comentarios_limpios = preprocesar_comentarios(comentarios)

        comentarios_analizados = analizar_sentimientos(comentarios_limpios)

        # 🔥 Conteo robusto (incluye errores)
        conteo = {
            "POS": 0,
            "NEG": 0,
            "NEU": 0,
            "ERROR": 0
        }

        for c in comentarios_analizados:
            sentimiento = c.get("sentimiento", "ERROR")

            if sentimiento in conteo:
                conteo[sentimiento] += 1
            else:
                conteo["ERROR"] += 1

        return {
            "url": solicitud.url,
            "total_comentarios": len(comentarios_analizados),
            "resumen": conteo,
            "comentarios": comentarios_analizados
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))