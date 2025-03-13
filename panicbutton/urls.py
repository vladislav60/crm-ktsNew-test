from django.urls import path
from .views import *

urlpatterns = [
    path('send_alarm/', send_alarm, name='send_alarm'),
    path('get_alarms/', get_alarms, name='get_alarms'),
    path('create_alarm/', create_alarm, name='create_alarm'),
    path("map/", panic_map_view, name="map"),
    path("testmap/", test_panic_map_view, name="testmap"),
    path('api/get_key/', get_api_key, name='get_api_key'),
    path('api/request_new_key/', request_new_key, name='request_new_key'),
    path('api/update_key/<int:user_id>/', update_api_key, name='update_api_key'),
    path('api/revoke_key/<int:user_id>/', revoke_api_key, name='revoke_api_key'),
    path('alarms/', alarms_view, name='alarms'),
    path('clients/', get_clients, name='get_clients'),
    path("update_alarm_status/<int:alarm_id>/", update_alarm_status, name="update_alarm_status"),
    path('client/<int:client_id>/', get_client, name='get_client'),
    path('login/', login_with_api_key, name='login_with_api_key'),
]