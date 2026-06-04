import requests
from app.config.settings import SAUCENAO_API_KEY
import logging

logger = logging.getLogger(__name__)

MIN_SAUCENAO_SIMILARITY = 50

def build_error_response(error_code, message):
    return {
        "success": False,
        "error_code": error_code,
        "message": message
    }

def build_saucenao_response(best_result):
    similarity = float(best_result["header"]["similarity"])
    print(f"SIMILARIDADE RETORNADA PELO SAUCENAO {similarity}")
    saucenao_data = best_result["data"]
    anime_title = saucenao_data.get("source")
    has_anilist_id = saucenao_data.get("anilist_id")    
    logger.info(f"Título retornado pelo SauceNAO: {anime_title}")
    logger.info(f"AniList ID retornado pelo SauceNAO: {has_anilist_id}")

    if not anime_title:
        return build_error_response(
            "NO_RESULT",
            "Não encontramos nenhuma obra correspondente para esta imagem."
        )
    
    '''if not has_anilist_id:
        return build_error_response(
            "NO_RESULT",
            "Não encontramos nenhuma obra correspondente para esta imagem."
        )'''
    
    if similarity < MIN_SAUCENAO_SIMILARITY:
        return build_error_response(
            "LOW_CONFIDENCE",
            "Não encontramos nenhuma obra correspondente para esta imagem."
        )
    
    return {
        "success": True,
        "data": {
            "anime": anime_title,
            "episode": saucenao_data.get("part"),
            "timestamp": saucenao_data.get("est_time"),
            "similarity": similarity
        }
    }

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
            
            results = data.get("results", [])

            if not results:
                return build_error_response(
                    "NO_RESPONSE",
                    "Não encontramos nenhuma obra correspondente para esta imagem."
                )
            
            best_result = results[0]

            return build_saucenao_response(best_result)

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