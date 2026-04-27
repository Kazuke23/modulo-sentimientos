# Script de prueba de conexión con Apify

from apify_client import ApifyClient
from dotenv import load_dotenv
import os
import json

# Cargar variables del archivo .env
load_dotenv()

def test_conexion_apify():
    token = os.getenv('APIFY_API_TOKEN')

    if not token:
        print('ERROR: No se encontró APIFY_API_TOKEN en el archivo .env')
        return

    print(f'Token encontrado: {token[:20]}...')
    print('Conectando con Apify...')

    client = ApifyClient(token)

    # URL de post público de prueba
    # Puedes cambiarla por cualquier post público de Facebook
    url_post = 'https://www.facebook.com/photo/?fbid=1426679685922698&set=a.536963958227613'

    print(f'Extrayendo comentarios de: {url_post}')
    print('(Esto puede tardar 1-2 minutos...)')

    run = client.actor('apify/facebook-comments-scraper').call(
        run_input={
            'startUrls': [{'url': url_post}],
            'maxComments': 10  # Solo 10 para la prueba
        }
    )

    comentarios = list(
        client.dataset(run['defaultDatasetId']).iterate_items()
    )

    print(f'\n✅ CONEXION EXITOSA — Se extrajeron {len(comentarios)} comentarios')
    print('\nPrimeros 3 comentarios:')
    for i, c in enumerate(comentarios[:3]):
        texto = c.get('text', '(sin texto)')
        print(f'  {i+1}. {texto[:100]}')

    # Guardar resultado en un archivo JSON
    with open('resultado_prueba.json', 'w', encoding='utf-8') as f:
        json.dump(comentarios, f, ensure_ascii=False, indent=2)
    print('\nResultado guardado en: backend/resultado_prueba.json')

if __name__ == '__main__':
    test_conexion_apify()
