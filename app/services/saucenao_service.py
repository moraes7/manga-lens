import requests
from app.config.settings import SAUCENAO_API_KEY

def search_cover_on_saucenao(image_path):
    if not SAUCENAO_API_KEY:
        return {
            "error": "SAUCENAO_API_KEY não encontrada"
        }
    
    params = {
        "api_key": SAUCENAO_API_KEY,
        "output_type": 2
    }

    with open(image_path, "rb") as image_file:
        response = requests.post(
            "https://saucenao.com/search.php",
            data=params,
            files={"file": image_file}
        )
        data = response.json()
        return data
