
from django.urls import path
from panicbutton.consumers import AlarmConsumer

websocket_urlpatterns = [
    path("ws/alarms/", AlarmConsumer.as_asgi()),  # 🔥 ВАЖНО! ws/alarms/
]
