from django.urls import path
from .views import map_view, place_details_api

urlpatterns = [
    path('', map_view),
    path('api/place-details/', place_details_api),
]
