import requests
import re
import logging


ANILIST_API_URL = "https://graphql.anilist.co"

logger = logging.getLogger(__name__)

def remove_season_suffix(anime_title):
    return re.sub(r"\s+S\d+$", "", anime_title).strip()

def clean_title_for_anilist(anime_title):
    title = re.sub(r"\(\d{4}\)", "", anime_title)
    title = title.replace("`", "")

    return title.strip()

def normalize_title(title):
    if not title:
        return ""
    
    return title.strip().lower()

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

def search_anilist_id(anime_title):
    query = """
    query ($search: String) {
        Media(search: $search, type: ANIME) {
            id
        }
    }
    """

    try:
        cleaned_title = clean_title_for_anilist(anime_title)
        media = fetch_anilist_media(cleaned_title, query)

        if not media:
            return None
        
        return media.get("id")
    except requests.exceptions.Timeout:
        return None

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
        cleaned_title = clean_title_for_anilist(anime_title)
        media = fetch_anilist_media(cleaned_title, query)

        if not media:
            fallback_title = remove_season_suffix(cleaned_title)

            if normalize_title(fallback_title) != normalize_title(anime_title):
                logger.info(f"TENTANDO BUSCA ALTERNATIVA: {fallback_title}")

                media = fetch_anilist_media(fallback_title, query)

            if not media:
                return None

        return media.get("coverImage", {}).get("large")
    
    except requests.exceptions.Timeout:
        return None