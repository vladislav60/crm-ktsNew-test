
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ktscrm.settings')
django.setup()


from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from panicbutton.routing import websocket_urlpatterns
from panicbutton.middleware import TokenAuthMiddlewareStack


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})