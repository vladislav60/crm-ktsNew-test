# panicbutton/middleware.py
from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user_by_token(token_key):
    from panicbutton.models import APIKey
    try:
        api_key = APIKey.objects.get(key=token_key)
        if api_key.is_valid():
            return api_key.user
        return AnonymousUser()
    except APIKey.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    ASGI middleware that authenticates WebSocket connections using ?token=...
    """

    def __init__(self, app):
        self.app = app  # ASGI app

    async def __call__(self, scope, receive, send):
        # Только WebSocket
        if scope["type"] == "websocket":
            query_string = parse_qs(scope.get("query_string", b"").decode())
            token_key = query_string.get("token", [None])[0]

            user = await get_user_by_token(token_key)
            scope["user"] = user

        return await self.app(scope, receive, send)


def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)