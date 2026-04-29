# backend/scraper.py
from apify_client import ApifyClient
from dotenv import load_dotenv
import os

load_dotenv()

def extraer_comentarios(url_post: str, max_comentarios: int = 10):
    token = os.getenv("APIFY_API_TOKEN")
    client = ApifyClient(token)

    if "instagram.com" in url_post:
        run = client.actor("apify/instagram-comment-scraper").call(
            run_input={
                "directUrls": [url_post],
                "resultsLimit": max_comentarios,
            }
        )
        comentarios = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            comentarios.append({
                "texto": item.get("text", ""),
                "autor": item.get("ownerUsername", ""),
                "fecha": item.get("timestamp", ""),
                "likes": item.get("likesCount", 0)
            })
    else:
        run = client.actor("apify/facebook-comments-scraper").call(
            run_input={
                "startUrls": [{"url": url_post}],
                "maxComments": max_comentarios,
                "maxReplies": 0,
            }
        )
        comentarios = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            comentarios.append({
                "texto": item.get("text", ""),
                "autor": item.get("authorName", ""),
                "fecha": item.get("date", ""),
                "likes": item.get("likesCount", 0)
            })

    return comentarios[:max_comentarios]