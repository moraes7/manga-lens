import requests
import re

MIN_SIMILARITY = 88

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


def search_anime_by_image(image_path):
    url = "https://api.trace.moe/search"

    try:
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                url,
                files={'image': image_file},
                timeout=10
            )

        if response.status_code != 200:
            return {
                "success": False,
                "message": "Erro ao consultar a API do trace.moe"
            }

        data = response.json()

        if "result" not in data:
            return {
                "success": False,
                "message": "Resposta inválida da API"
            }

        if not data['result']:
            return {
                "success": False,
                "message": "Nenhum resultado encontrado"
            }

        best_result = data['result'][0]

        cleaned_title = clean_anime_title(
            best_result.get("filename", "")
        )

        similarity = round(
            best_result.get("similarity", 0) * 100,
            2
        )

        if similarity < MIN_SIMILARITY:
            return {
                "success": False,
                "message": "Resultado com baixa confiança"
            }

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

    except FileNotFoundError:
        return {
            "success": False,
            "message": "Imagem não encontrada"
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "A API demorou muito para responder"
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "message": "Não foi possível conectar à API"
        }

    except requests.exceptions.RequestException:
        return {
            "success": False,
            "message": "Erro na requisição para a API"
        }

    except Exception:
        return {
            "success": False,
            "message": "Erro inesperado ao buscar anime pela imagem"
        }