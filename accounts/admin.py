from django.contrib import admin
from accounts.models import UserProfile
# Register your models here.
from .models import *

# Register your models here.
admin.site.register(UserProfile)