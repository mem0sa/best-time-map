import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .services.google_places import search_organizations
from .services.google_place_details import get_place_details
from django.conf import settings

def map_view(request):
    return render(request, 'locations/map.html', {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    })


@csrf_exempt
def location_click_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        lat = data.get('lat')
        lon = data.get('lon')

        organizations = search_organizations(lat, lon)

        return JsonResponse({
            'status': 'ok',
            'organizations': organizations
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def place_details_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        place_id = data.get("place_id")

        details = get_place_details(place_id)

        return JsonResponse({
            "status": "ok",
            "details": details
        })

    return JsonResponse({"error": "Invalid request"}, status=400)