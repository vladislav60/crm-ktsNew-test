from datetime import timedelta, datetime

from django.contrib import admin
from django.utils.timezone import now

from .models import Operator, Alarm, ClientProfile, APIKey


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_operator')
    list_filter = ('is_operator',)
    search_fields = ('user__username',)


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display = ('client', 'latitude', 'longitude', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('client__username', 'status')

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'last_alarm_at')
    search_fields = ('user__username', 'phone_number', 'address')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not APIKey.objects.filter(user=obj.user).exists():
            APIKey.objects.create(user=obj.user, expires_at=datetime.now() + timedelta(days=365))


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'expires_at', 'is_valid')
    actions = ['regenerate_api_key', 'revoke_api_key', 'restore_api_keys']
    search_fields = ('user__username', 'key')
    list_filter = ('expires_at',)

    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True  # Отображаем как иконку ✅/❌

    @admin.action(description="🔄 Обновить API-ключ (создать новый)")
    def regenerate_api_keys(self, request, queryset):
        """Генерирует новый API-ключ для выбранных пользователей"""
        for api_key in queryset:
            api_key.regenerate_key()
        self.message_user(request, f"Обновлено {queryset.count()} API-ключ(ей).")

    @admin.action(description="♻️ Восстановить API-ключ (продлить срок)")
    def restore_api_keys(self, request, queryset):
        """Восстанавливает API-ключ, продлевая срок без изменения ключа"""
        count = 0
        for api_key in queryset:
            if not api_key.is_valid():
                api_key.restore_key()
                count += 1
        self.message_user(request, f"Восстановлено {count} API-ключ(ей).")

    @admin.action(description="Отозвать API-ключ")
    def revoke_api_key(self, request, queryset):
        for api_key in queryset:
            api_key.revoke_key()
        self.message_user(request, "API-ключи успешно отозваны.")