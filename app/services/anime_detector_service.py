from app.integrations.trace_moe import search_anime_by_image
from app.integrations.anilist import search_anime_cover
from app.services.saucenao_service import search_cover_on_saucenao

MIN_SAUCENAO_SIMILARITY = 60

def detect_anime(original_image_path, processed_image_path):
    trace_moe_result = search_anime_by_image(processed_image_path)

    if trace_moe_result["success"] and trace_moe_result["data"]:

        anime_title = trace_moe_result["data"]["anime"]

        cover_url = search_anime_cover(anime_title)

        trace_moe_result["data"]["cover_url"] = cover_url

        trace_moe_result["source"] = "trace.moe"

        return trace_moe_result

    saucenao_result = search_cover_on_saucenao(original_image_path)

    results = saucenao_result.get("results", [])

    if not results:
        return {
            "success": False,
            "error_code": "NO_RESULT",
            "message": "Não encontramos nenhuma obra correspondente para esta imagem."
        }

    best_result = results[0]

    similarity = float(best_result["header"]["similarity"])

    saucenao_data = best_result["data"]

    anime_title = saucenao_data.get("source")

    has_anilist_id = saucenao_data.get("anilist_id") 

    if not anime_title:
        return {
            "success": False,
            "error_code": "NO_RESULT",
            "message": "Não conseguimos identificar a obra desta imagem."
        }
    
    if not has_anilist_id:  
        return {  
            "success": False,
            "error_code": "NO_RESULT",
            "message": "Não conseguimos identificar a obra desta imagem."
        }

    if similarity < MIN_SAUCENAO_SIMILARITY:
        return {
            "success": False,
            "error_code": "LOW_CONFIDENCE",
            "message": "Não conseguimos identificar a obra desta imagem."
        }
    
    cover_url = search_anime_cover(anime_title)

    return {
        "success": True,
        "source": "saucenao",
        "data": { 
            "anime": anime_title,  
            "episode": saucenao_data.get("part"),
            "timestamp": saucenao_data.get("est_time"),
            "similarity": similarity,
            "cover_url": cover_url
        }
}