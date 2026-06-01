import requests
import re
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s"
)

logger = logging.getLogger(__name__)

MIN_SIMILARITY = 80

ERROR_STATUS_MAP = {
    "INVALID_API_RESPONSE": 502,
    "NO_RESULT": 404,
    "LOW_CONFIDENCE": 422,
    "IMAGE_NOT_FOUND": 400,
    "API_TIMEOUT": 504,
    "API_CONNECTION_ERROR": 502,
    "API_REQUEST_ERROR": 502,
    "UNEXPECTED_ERROR": 500
}


def clean_anime_title(filename):

    filename = re.sub(r"\[.*?\]", "", filename)

    filename = re.sub(r"\(.*?p\)", "", filename)

    filename = re.sub(r"\.(mkv|mp4|avi)$", "", filename)

    filename = filename.strip()

    filename = re.sub(r"\s*-\s*\d+\s*$", "", filename)

    filename = re.sub(r"\s+", " ", filename)

    return filename.strip()


def format_timestamp(seconds):

    minutes = int(seconds // 60)

    remaining_seconds = int(seconds % 60)

    return f"{minutes:02}:{remaining_seconds:02}"

def build_error_response(error_code, message):
    logger.warning(f"Error: {error_code} - {message}")

    return {
        "success": False,
        "error_code": error_code,
        "message": message
    }


def validate_trace_result(data):

    if "result" not in data:
        return build_error_response(
            "INVALID_API_RESPONSE",
            "Não conseguimos interpretar a resposta do serviço de identificação."
        )

    if not data['result']:
        return build_error_response(
            "NO_RESULT",
            "Não encontramos nenhuma obra correspondente para esta imagem."
        )

    best_result = data['result'][0]

    similarity = round(
        best_result.get("similarity", 0) * 100,
        2
    )
    logger.info(f"Similaridade retornada pelo trace.moe: {similarity}%")

    if similarity < MIN_SIMILARITY:
        return build_error_response(
            "LOW_CONFIDENCE",
            "Não conseguimos identificar a obra desta imagem."
        )
    
    logger.info(f" Resultado aceito com similaridade de: {similarity}%")

    return {
        "success": True,
        "result": best_result
    }


def build_trace_response(best_result):

    cleaned_title = clean_anime_title(
        best_result.get("filename", "")
    )

    similarity = round(
        best_result.get("similarity", 0) * 100,
        2
    )

    formatted_timestamp = format_timestamp(
        best_result.get("from", 0)
    )

    return {
        "success": True,
        "data": {
            "anime": cleaned_title,
            "episode": best_result.get("episode"),
            "similarity": similarity,
            "timestamp": formatted_timestamp,
            "preview": best_result.get("image")
        }
    }


def search_anime_by_image(image_path):
    url = "https://api.trace.moe/search"

    try:
        logger.info(f" Enviando imagem para API do trace.moe: {image_path}")

        with open(image_path, 'rb') as image_file:
            response = requests.post(
                url,
                files={'image': image_file},
                timeout=10
            )

        if response.status_code != 200:
            return build_error_response(
                "API_REQUEST_ERROR",
                "Erro ao consultar a API do trace.moe"
            )

        data = response.json()

        validation = validate_trace_result(data)

        if not validation["success"]:
            return validation

        best_result = validation["result"]

        return build_trace_response(best_result)

    except FileNotFoundError:
        return build_error_response(
            "IMAGE_NOT_FOUND",
            "Não conseguimos encontrar a imagem enviada."
        )

    except requests.exceptions.Timeout:
        return build_error_response(
            "API_TIMEOUT",
            "O serviço de identificação demorou demais para responder."
        )

    except requests.exceptions.ConnectionError:
        return build_error_response(
            "API_CONNECTION_ERROR",
            "Não conseguimos conectar ao serviço de identificação agora."
        )

    except requests.exceptions.RequestException:
        return build_error_response(
            "API_REQUEST_ERROR",
            "Não foi possível consultar o serviço de identificação neste momento."
        )

    except Exception:
        logger.exception("Erro inesperado ao buscar anime pela imagem")

        return build_error_response(
            "UNEXPECTED_ERROR",
            "Algo inesperado aconteceu durante a identificação da imagem."
        )