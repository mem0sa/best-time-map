import requests
from django.conf import settings

def search_organizations(lat, lon, radius=500):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "key": settings.GOOGLE_MAPS_API_KEY,
        "location": f"{lat},{lon}",
        "radius": radius,
        "type": "establishment"
    }

    response = requests.get(url, params=params)
    data = response.json()

    organizations = []

    for place in data.get("results", []):
        organizations.append({
            "id": place.get("place_id"),
            "name": place.get("name"),
            "address": place.get("vicinity"),
            "lat": place["geometry"]["location"]["lat"],
            "lon": place["geometry"]["location"]["lng"],
            "rating": place.get("rating"),
        })

    return organizations
