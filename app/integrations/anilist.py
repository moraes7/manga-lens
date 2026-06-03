import requests
import re
import logging


ANILIST_API_URL = "https://graphql.anilist.co"

logger = logging.getLogger(__name__)

def remove_season_suffix(anime_title):
    return re.sub(r"\s+S\d+$", "", anime_title).strip()

def fetch_anilist_media(anime_title, query):
    variables = {
        "search": anime_title,
    }
    logger.info(f"BUSCANDO CAPA PARA: {anime_title}")

    response = requests.post(
        ANILIST_API_URL,
        json={
            "query": query,
            "variables": variables
        },
        timeout=10
    )
    data = response.json()

    return data.get("data", {}).get("Media")

def search_anime_cover(anime_title):
    query = """
    query ($search: String) {
        Media(search: $search, type: ANIME) {
            coverImage {
                large
            }
        }
    }
    """

    try:
        media = fetch_anilist_media(anime_title, query)

        if not media:
            fallback_title = remove_season_suffix(anime_title)
            logger.info(f"TENTANDO BUSCA ALTERNATIVA: {fallback_title}")

            media = fetch_anilist_media(fallback_title, query)

            if not media:
                return None

        return media.get("coverImage", {}).get("large")
    
    except requests.exceptions.Timeout:
        return None