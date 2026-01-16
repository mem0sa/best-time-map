import requests
from django.conf import settings


def get_place_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "key": settings.GOOGLE_MAPS_API_KEY,
        "place_id": place_id,
        "language":"ru",
        "fields": (
            "name,"
            "rating,"
            "user_ratings_total,"
            "opening_hours,"
            "types,"
            "formatted_address"
        )
    }

    response = requests.get(url, params=params)
    data = response.json()

    result = data.get("result", {})

    return {
        "name": result.get("name"),
        "address": result.get("formatted_address"),
        "rating": result.get("rating"),
        "reviews_count": result.get("user_ratings_total"),
        "opening_hours": result.get("opening_hours", {}).get("weekday_text"),
        "types": result.get("types"),
    }
