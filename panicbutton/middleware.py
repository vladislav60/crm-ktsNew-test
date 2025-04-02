# panicbutton/middleware.py
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack

@database_sync_to_async
def get_user(token_key):
    from panicbutton.models import APIKey  # перенесите сюда
    from django.contrib.auth.models import AnonymousUser  # перенесите сюда
    try:
        api_key = APIKey.objects.get(key=token_key)
        return api_key.user
    except APIKey.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self.inner)

class TokenAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = scope
        self.inner = inner

    async def __call__(self, receive, send):
        query_string = parse_qs(self.scope["query_string"].decode())
        token_key = query_string.get('token', [None])[0]
        self.scope['user'] = await get_user(token_key)
        inner = self.inner(self.scope)
        return await inner(receive, send)

def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))