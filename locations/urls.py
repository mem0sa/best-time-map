from django.urls import path
from .views import map_view, location_click_api, place_details_api

urlpatterns = [
    path('', map_view),
    path('api/location/', location_click_api),
    path('api/place-details/', place_details_api),
]
