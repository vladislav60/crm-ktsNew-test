from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'accounts'

    @classmethod
    def create_profile_for_user(cls, user):
        profile, created = cls.objects.get_or_create(user=user)
        return profile