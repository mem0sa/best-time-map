from django.urls import path
from .views import map_view, location_click_api

urlpatterns = [
    path('', map_view, name='map'),
    path('api/location/', location_click_api, name='location_api'),
]
