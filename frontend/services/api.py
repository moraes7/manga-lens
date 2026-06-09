import requests

API_URL = "https://manga-lens.onrender.com/docs"

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

    return response.json()