import requests
from django.conf import settings


def search_organizations(lat, lon, radius=500):
    url = 'https://search-maps.yandex.ru/v1/'

    params = {
        'apikey': settings.YANDEX_API_KEY,
        'lang': 'ru_RU',
        'll': f'{lon},{lat}',
        'spn': '0.01,0.01',
        'type': 'biz',
        'results': 20
    }

    response = requests.get(url, params=params)

    print('YANDEX STATUS:', response.status_code)
    print('YANDEX RESPONSE:', response.text[:500])
    

    data = response.json()
    
    organizations = []

    for feature in data.get('features', []):
        properties = feature['properties']
        geometry = feature['geometry']

        organizations.append({
            'id': properties.get('CompanyMetaData', {}).get('id'),
            'name': properties.get('name'),
            'category': properties.get('CompanyMetaData', {}).get('Categories', [{}])[0].get('name'),
            'address': properties.get('CompanyMetaData', {}).get('address'),
            'lat': geometry['coordinates'][1],
            'lon': geometry['coordinates'][0],
        })

    return organizations
