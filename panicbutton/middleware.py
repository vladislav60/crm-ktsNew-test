# panicbutton/middleware.py
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user_by_token(token_key):
    from panicbutton.models import APIKey  # импортируем внутри функции
    try:
        api_key = APIKey.objects.get(key=token_key)
        if api_key.is_valid():  # твоя проверка срока действия токена
            return api_key.user
        return AnonymousUser()
    except APIKey.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    """ASGI middleware for token-only authentication."""

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self.inner)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = scope
        self.inner = inner

    async def __call__(self, receive, send):
        query_string = self.scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token_key = query_params.get("token", [None])[0]

        if token_key:
            self.scope["user"] = await get_user_by_token(token_key)
        else:
            self.scope["user"] = AnonymousUser()

        # запускаем следующий обработчик
        inner = self.inner(self.scope)
        return await inner(receive, send)


def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)