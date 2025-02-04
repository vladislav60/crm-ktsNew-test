from django.urls import path
from .views import *

urlpatterns = [
    path('send_alarm/', send_alarm, name='send_alarm'),
    path('get_alarms/', get_alarms, name='get_alarms'),
    path("map/", panic_map_view, name="map"),
]