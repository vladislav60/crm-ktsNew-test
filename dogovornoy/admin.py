from django.contrib import admin

# Register your models here.
from .models import *

class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ('kts', 'service_name', 'price', 'date_added')

@admin.register(kts)
class ktsAdmin(admin.ModelAdmin):
    list_display = (
    'dogovor_number', 'object_number', 'klient_name', 'adres', 'telephone', 'iin_bin')
    list_display_links = ('dogovor_number', 'object_number')
    search_fields = ('dogovor_number', 'object_number')
    list_per_page = 8

@admin.register(partners_object)
class PartnersObjectAdmin(admin.ModelAdmin):
    list_display = ('object_number', 'gsm_number', 'name_object', 'adres', 'type_object', 'vid_sign', 'hours_mounth', 'date_podkluchenia', 'tariff_per_mounth', 'tehnical_services', 'rent_gsm', 'fire_alarm', 'telemetria', 'nabludenie', 'sms_uvedomlenie', 'kolvo_day', 'primechanie', 'ekipazh', 'urik', 'company_name')
    search_fields = ('object_number', 'name_object', 'adres')
    list_per_page = 8  # Количество объектов на странице

@admin.register(partners_rekvizity)
class PartnersRekvizityAdmin(admin.ModelAdmin):
    list_display = ('id', 'polnoe_name', 'adres_company', 'bin', 'iban', 'bic', 'bank', 'telephone_ofiice', 'telephone_buh', 'vid_too', 'doljnost', 'ucheriditel_name_polnoe', 'ucheriditel_name_sokr')
    search_fields = ('polnoe_name', 'adres_company', 'bin')
    list_filter = ('vid_too',)


@admin.register(rekvizity)
class rekvizity(admin.ModelAdmin):
    list_display = ('id', 'polnoe_name', 'adres_company', 'bin', 'iban', 'bic', 'bank', 'telephone_ofiice', 'telephone_buh', 'vid_too', 'doljnost', 'ucheriditel_name_polnoe', 'ucheriditel_name_sokr')
    search_fields = ('polnoe_name', 'adres_company', 'bin')
    list_filter = ('vid_too',)


@admin.register(vid_sign)
class VidSignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_sign', 'name_sign_polnoe')
    search_fields = ('id',)


@admin.register(ekipazh)
class EkipazhAdmin(admin.ModelAdmin):
    list_display = ('id', 'ekipazh_name',)
    search_fields = ('id',)


# Регистрация Базы клиентов договорного в админке
# admin.site.register(ktsAdmin)
# admin.site.register(rekvizity)
admin.site.register(AdditionalService, AdditionalServiceAdmin)