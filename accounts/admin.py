from django.contrib import admin
from accounts.models import UserProfile
# Register your models here.
from .models import *

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):  # Изменил на ModelAdmin
    list_display = ('user', 'department')  # Исправил дублирование department

admin.site.register(UserProfile, UserProfileAdmin)