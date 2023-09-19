from django.contrib import admin

# Register your models here.
from .models import *

class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ('kts', 'service_name', 'price', 'date_added')

class ktsAdmin(admin.ModelAdmin):
    list_display = (
    'dogovor_number', 'object_number', 'klient_name', 'adres', 'telephone', 'itog_oplata', 'iin_bin')
    list_display_links = ('dogovor_number', 'object_number')
    search_fields = ('dogovor_number', 'object_number')


# Регистрация Базы клиентов договорного в админке
admin.site.register(kts, ktsAdmin)
admin.site.register(rekvizity)
admin.site.register(vid_sign)
admin.site.register(AdditionalService, AdditionalServiceAdmin)