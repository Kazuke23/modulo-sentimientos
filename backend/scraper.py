# backend/scraper.py
from apify_client import ApifyClient
from dotenv import load_dotenv
import os

def extraer_comentarios(url_post: str, max_comentarios: int = 10):
    token = os.getenv("APIFY_API_TOKEN")
    client = ApifyClient(token)

    comentarios = []

    if "instagram.com" in url_post:
        run = client.actor("apify/instagram-comment-scraper").call(
            run_input={
                "directUrls": [url_post],
                "resultsLimit": max_comentarios,
            }
        )

        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        for item in items:
            comentarios.append({
                "texto": item.get("text", item.get("comment", item.get("commentText", ""))),
                "autor": item.get("ownerUsername", item.get("username", "")),
                "fecha": item.get("timestamp", item.get("date", item.get("createdAt", ""))),
                "likes": item.get("likesCount", item.get("likes", 0))
            })

    else:
        run = client.actor("apify/facebook-comments-scraper").call(
            run_input={
                "startUrls": [{"url": url_post}],
                "maxComments": max_comentarios,
                "maxReplies": 0,
            }
        )

        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        for item in items:
            comentarios.append({
                "texto": item.get("text", ""),
                "autor": item.get("authorName", ""),
                "fecha": item.get("date", ""),
                "likes": item.get("likesCount", 0)
            })

    return comentarios[:max_comentarios]