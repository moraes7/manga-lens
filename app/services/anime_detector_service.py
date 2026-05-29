from app.integrations.trace_moe import search_anime_by_image
from app.integrations.anilist import search_anime_cover
from app.services.saucenao_service import search_cover_on_saucenao


def detect_anime(image_path):
    trace_moe_result = search_anime_by_image(image_path)

    if trace_moe_result["success"] and trace_moe_result["data"]:

        anime_title = trace_moe_result["data"]["anime"]

        cover_url = search_anime_cover(anime_title)

        trace_moe_result["data"]["cover_url"] = cover_url

        trace_moe_result["source"] = "trace.moe"

        return trace_moe_result

    saucenao_result = search_cover_on_saucenao(image_path)

    results = saucenao_result.get("results", [])

    if not results:
        return {
            "success": False,
            "message": "Nunhum resultado encontrado no SauceNAO"
        }

    best_result = results[0]

    similarity = float(best_result["header"]["similarity"])

    if similarity < 70:
        return {
            "success": False,
            "message": "Resultado encontrado com baixa similaridade"
        }

    return {
        "success": True,
        "source": "saucenao",
        "result": saucenao_result
    }