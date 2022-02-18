import requests

API_URL = " https://api.punkapi.com/v2/beers"


def get_beers(url: str = API_URL) -> bytes:
    response = requests.get(url)
    return response.content
