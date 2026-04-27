# backend/preprocesador.py
import re

def limpiar_texto(texto: str) -> str:
    if not texto:
        return ""
    
    # Quitar URLs
    texto = re.sub(r'http\S+|www\S+', '', texto)
    
    # Quitar menciones @usuario
    texto = re.sub(r'@\w+', '', texto)
    
    # Quitar emojis y caracteres especiales no alfabéticos
    texto = re.sub(r'[^\w\sáéíóúñüÁÉÍÓÚÑÜ.,!?]', '', texto)
    
    # Quitar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

def preprocesar_comentarios(comentarios: list) -> list:
    procesados = []
    for c in comentarios:
        texto_limpio = limpiar_texto(c.get("texto", ""))
        if texto_limpio:  # Ignorar comentarios vacíos tras limpiar
            procesados.append({
                "texto_original": c.get("texto", ""),
                "texto_limpio": texto_limpio,
                "autor": c.get("autor", ""),
                "fecha": c.get("fecha", ""),
                "likes": c.get("likes", 0)
            })
    return procesados