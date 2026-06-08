from app.integrations.trace_moe import search_anime_by_image
from app.integrations.anilist import search_anime_cover, search_anilist_id
from app.integrations.saucenao import search_cover_on_saucenao
import logging

logger = logging.getLogger(__name__)

def normalize_title(title):
    if not title:
        return ""
    
    return title.lower().strip()

def have_same_anilist_id(trace_result, saucenao_result):
    trace_anilist_id = trace_result["data"].get("anilist_id")
    saucenao_anilist_id = saucenao_result["data"].get("anilist_id")

    if not trace_anilist_id or not saucenao_anilist_id:
        return False

    return trace_anilist_id == saucenao_anilist_id

def fill_missing_saucenao_anilist_id(saucenao_result):
    if saucenao_result["data"].get("anilist_id"):
        return saucenao_result
    
    work_title = saucenao_result["data"].get("title") or saucenao_result["data"].get("anime")
    saucenao_result["data"]["anilist_id"] = search_anilist_id(work_title)

    return saucenao_result

def copy_trace_episode_data(saucenao_result, trace_result):
    saucenao_result["data"]["episode"] = trace_result["data"].get("episode")
    saucenao_result["data"]["timestamp"] = trace_result["data"].get("timestamp")

    return saucenao_result


def enrich_anime_result(result, source):
    work_title = result["data"].get("title") or result["data"].get("anime") 
    cover_url = search_anime_cover(work_title)
    result["data"]["cover_url"] = cover_url
    result["source"] = source

    return result


def detect_anime(original_image_path, processed_image_path):
    trace_moe_result = search_anime_by_image(processed_image_path)

    saucenao_result = search_cover_on_saucenao(original_image_path)

    logger.info(f"Trace.moe result: {trace_moe_result}")
    logger.info(f"SauceNAO result: {saucenao_result}")

    if saucenao_result["success"]:
        saucenao_result = fill_missing_saucenao_anilist_id(saucenao_result)

        if trace_moe_result["success"] and have_same_anilist_id(trace_moe_result, saucenao_result):
            saucenao_result = copy_trace_episode_data(saucenao_result, trace_moe_result)
        
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