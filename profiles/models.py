from django.db import models
from django.contrib.auth.models import User
from avatar.models import Avatar, AvatarField
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = AvatarField(upload_to='avatars', null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
