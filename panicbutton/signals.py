import secrets
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from datetime import datetime, timedelta


@receiver(post_save, sender=ClientProfile)
def create_api_key(sender, instance, created, **kwargs):
    """ Создание API-ключа при создании нового клиента """
    if created:
        APIKey.objects.create(
            user=instance.user,
            key=secrets.token_urlsafe(32),
            expires_at=datetime.now() + timedelta(days=365),
        )