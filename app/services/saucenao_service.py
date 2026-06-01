import requests
from app.config.settings import SAUCENAO_API_KEY

def search_cover_on_saucenao(image_path):
    if not SAUCENAO_API_KEY:
        return {
             "success": False,
            "error_code": "MISSING_API_KEY", 
            "message": "O serviço de identificação não está configurado corretamente."
        }
    
    params = {
        "api_key": SAUCENAO_API_KEY,
        "output_type": 2
    }

    try:
        with open(image_path, "rb") as image_file:
            response = requests.post(
                "https://saucenao.com/search.php",
                data=params,
                files={"file": image_file},
                timeout=10
            )
            data = response.json()
            return data
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error_code": "API_TIMEOUT",
            "message": "O serviço de identificação demorou demais para responder."
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error_code": "API_CONNECTION_ERROR",
            "message": "Não conseguimos conectar ao serviço de identificação agora."
        } 
    except requests.exceptions.RequestException:
        return {  
            "success": False,
            "error_code": "API_REQUEST_ERROR",
            "message": "Não foi possível consultar o serviço de identificação neste momento."
        } 