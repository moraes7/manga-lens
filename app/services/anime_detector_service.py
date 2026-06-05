from app.integrations.trace_moe import search_anime_by_image
from app.integrations.anilist import search_anime_cover
from app.services.saucenao_service import search_cover_on_saucenao
import logging

logger = logging.getLogger(__name__)

def enrich_anime_result(result, source):
    anime_title = result["data"]["anime"]
    cover_url = search_anime_cover(anime_title)
    result["data"]["cover_url"] = cover_url
    result["source"] = source

    return result


def detect_anime(original_image_path, processed_image_path):
    trace_moe_result = search_anime_by_image(processed_image_path)

    saucenao_result = search_cover_on_saucenao(original_image_path)

    logger.info(f"Trace.moe result: {trace_moe_result}")
    logger.info(f"SauceNAO result: {saucenao_result}")

    if saucenao_result["success"]:
        return enrich_anime_result(
            saucenao_result,
            "saucenao"
        )
    
    if trace_moe_result["success"]:
        return enrich_anime_result(
            trace_moe_result,
            "trace.moe"
        )
    
    return {
        "success": False,
        "error_code": "NO_RESULT",
        "message": "Não encontramos nenhuma obra correspondente para esta imagem."
    }