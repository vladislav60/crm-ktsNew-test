from django import forms
from django.contrib.auth.models import User
from avatar.forms import PrimaryAvatarForm

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['department', 'avatar']


class AvatarForm(PrimaryAvatarForm):
    pass