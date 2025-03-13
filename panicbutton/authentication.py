from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import now
from .models import APIKey

class APIKeyAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        api_key = APIKey.objects.filter(key=key).first()

        if not api_key or not api_key.is_valid():
            raise AuthenticationFailed("Ваш API-ключ недействителен, обратитесь в поддержку.")

        return (api_key.user, None)
