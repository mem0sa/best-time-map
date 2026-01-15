import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .services.google_places import search_organizations
from .services.google_place_details import get_place_details
from .services.visit_recommendation import get_visit_recommendation
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
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        body = json.loads(request.body)
        place_id = body.get("place_id")

        if not place_id:
            return JsonResponse({"error": "place_id is required"}, status=400)

        details = get_place_details(place_id)

        recommendation = get_visit_recommendation(details)
        
        return JsonResponse({
            "status": "ok",
            "details": details,
            "recommendation": recommendation
        })

    except Exception as e:
        return JsonResponse(
            {"error": "Internal server error", "details": str(e)},
            status=500
        )