from app.integrations.trace_moe import search_anime_by_image
from app.integrations.anilist import search_anime_cover
from app.services.saucenao_service import search_cover_on_saucenao


def detect_anime(original_image_path, processed_image_path):
    trace_moe_result = search_anime_by_image(processed_image_path)

    saucenao_result = search_cover_on_saucenao(original_image_path)

    if saucenao_result["success"]:
        anime_title = saucenao_result["data"]["anime"]
        cover_url = search_anime_cover(anime_title)
        saucenao_result["data"]["cover_url"] = cover_url
        saucenao_result["source"] = "saucenao"

        return saucenao_result
    
    if trace_moe_result["success"]:
        anime_title = trace_moe_result["data"]["anime"]
        cover_url = search_anime_cover(anime_title)
        trace_moe_result["data"]["cover_url"] = cover_url
        trace_moe_result["source"] = "trace.moe"

        return trace_moe_result
    
    return {
        "success": False,
        "error_code": "NO_RESULT",
        "message": "Não encontramos nenhuma obra correspondente para esta imagem."
    }