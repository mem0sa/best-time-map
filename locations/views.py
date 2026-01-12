import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


def map_view(request):
    return render(request, 'locations/map.html')


@csrf_exempt
def location_click_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        lat = data.get('lat')
        lon = data.get('lon')

        print(f'Получены координаты: {lat}, {lon}')

        return JsonResponse({
            'status': 'ok',
            'lat': lat,
            'lon': lon
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)
