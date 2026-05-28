import requests
from app.config.settings import SAUCENAO_API_KEY

def search_cover_on_saucenao(image_url):
    if not SAUCENAO_API_KEY:
        return {
            "error": "SAUCENAO_API_KEY não encontrada"
        }
    
    params = {
        "api_key": SAUCENAO_API_KEY,
        "url": image_url,
        "output_type": 2
    }

    response = requests.get(
        "https://saucenao.com/search.php",
        params=params
    )

    data = response.json()
    
    return data
