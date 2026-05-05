from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import anthropic
from dotenv import load_dotenv

from backend.scraper import extraer_comentarios
from backend.preprocesador import preprocesar_comentarios
from backend.analizador import analizar_sentimientos

load_dotenv()

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

class Mensaje(BaseModel):
    role: str
    content: str

class SolicitudChat(BaseModel):
    mensajes: List[Mensaje]
    contexto: str

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando correctamente"}

@app.post("/analizar")
def analizar(solicitud: SolicitudAnalisis):
    if not solicitud.url:
        raise HTTPException(status_code=400, detail="URL requerida")
    try:
        comentarios = extraer_comentarios(solicitud.url, solicitud.max_comentarios)
        comentarios_limpios = preprocesar_comentarios(comentarios)
        comentarios_analizados = analizar_sentimientos(comentarios_limpios)

        conteo = {"POS": 0, "NEG": 0, "NEU": 0, "ERROR": 0}
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

@app.post("/chat")
def chat(solicitud: SolicitudChat):
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            system=solicitud.contexto,
            messages=[{"role": m.role, "content": m.content} for m in solicitud.mensajes]
        )
        return {"respuesta": response.content[0].text}
    except Exception as e:
        print(f"ERROR CHAT: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")