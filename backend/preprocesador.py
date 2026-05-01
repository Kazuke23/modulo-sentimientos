# backend/preprocesador.py

import re

def limpiar_texto(texto: str) -> str:
    if not texto:
        return ""
    
    # Quitar URLs
    texto = re.sub(r'http\S+|www\S+', '', texto)
    
    # Quitar menciones
    texto = re.sub(r'@\w+', '', texto)
    
    # ⚠️ MENOS AGRESIVO (no eliminar todo)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

def preprocesar_comentarios(comentarios: list) -> list:
    procesados = []

    for c in comentarios:
        texto_original = c.get("texto", "")
        texto_limpio = limpiar_texto(texto_original)

        # 🔥 NO FILTRAR
        procesados.append({
            "texto_original": texto_original,
            "texto_limpio": texto_limpio,
            "autor": c.get("autor", ""),
            "fecha": c.get("fecha", ""),
            "likes": c.get("likes", 0)
        })

    return procesados