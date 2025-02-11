import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import panicbutton.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ktscrm.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(panicbutton.routing.websocket_urlpatterns)
    ),
})