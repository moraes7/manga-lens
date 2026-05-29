import requests


ANILIST_API_URL = "https://graphql.anilist.co"

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

    variables = {
        "search": anime_title
    }

    response = requests.post(
        ANILIST_API_URL,
        json={
            "query": query,
            "variables": variables
        },
        timeout=10
    )

    data = response.json()

    media = data.get("data", {}).get("Media")

    if not media:
        return None

    return media.get("coverImage", {}).get("large")