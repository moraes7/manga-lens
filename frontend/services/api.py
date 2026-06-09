import requests

API_URL = "https://manga-lens.onrender.com/upload"

def analyze_image(uploaded_file):

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    response = requests.post(
        API_URL,
        files=files,
        timeout=30
    )

    response.raise_for_status()

    return response.json()