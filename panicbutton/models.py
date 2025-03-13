from django.db import models
from django.contrib.auth.models import User
import secrets
from datetime import timedelta, datetime
from django.utils.timezone import now


class Operator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_operator = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Alarm(models.Model):
    STATUS_CHOICES = [
        ("new", "Новая"),
        ('pending', 'Ожидает обработки'),
        ('in_progress', 'В работе'),
        ('resolved', 'Завершено'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время тревоги")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Обновляем last_alarm_at у ClientProfile
        client_profile = ClientProfile.objects.filter(user=self.client).first()
        if client_profile:
            client_profile.last_alarm_at = now()
            client_profile.save()

    def __str__(self):
        return f"Тревога от {self.client.username} ({self.get_status_display()})"


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Клиент")
    name_client = models.CharField(max_length=255, blank=True, verbose_name="Имя клиента")
    description = models.TextField(blank=True, verbose_name="Описание объекта")
    object_type = models.CharField(max_length=255, blank=True, verbose_name="Тип объекта")
    route_info = models.TextField(blank=True, verbose_name="Текстовое обозначение маршрута")
    floor = models.IntegerField(blank=True, null=True, verbose_name="Этаж")
    floor_total = models.IntegerField(blank=True, null=True, verbose_name="Этажей")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    contract = models.CharField(blank=True, max_length=50, verbose_name="Договор")
    address = models.CharField(blank=True, max_length=255, verbose_name="Адрес")
    arrival_time = models.CharField(blank=True, max_length=255, verbose_name="Время прибытия")
    technical_spec = models.CharField(blank=True, null=True, max_length=255, verbose_name="Техник")
    intercom_code = models.CharField(blank=True, null=True, max_length=255, verbose_name="Код домофона")
    ekipaz_panic = models.CharField(blank=True, max_length=255, verbose_name="Экипаж")
    # Новое поле для времени последней тревоги
    last_alarm_at = models.DateTimeField(null=True, blank=True, verbose_name="Последняя тревога")

    def __str__(self):
        return f"{self.user.username} - {self.address}"


class APIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Клиент")
    key = models.CharField(max_length=50, unique=True, verbose_name="API-ключ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    expires_at = models.DateTimeField(verbose_name="Действует до")

    def regenerate_key(self):
        """Обновляет API-ключ и продлевает срок действия"""
        self.key = secrets.token_urlsafe(32)  # Унифицированная генерация 32 символов
        self.expires_at = now() + timedelta(days=365)  # Новый срок действия (1 год)
        self.save()

    def revoke_key(self):
        """Отзывает ключ (делает недействительным)"""
        self.expires_at = now()  # Ставим дату истечения в текущий момент
        self.save()

    def restore_key(self):
        """Восстанавливает существующий ключ, продлевая срок действия"""
        if self.expires_at <= now():
            self.expires_at = now() + timedelta(days=365)  # Обновляем срок действия
            self.save()

    def save(self, *args, **kwargs):
        """Создаёт API-ключ и срок действия, если они отсутствуют"""
        if not self.key:
            self.key = secrets.token_urlsafe(32)  # Унифицированная генерация
        if not self.expires_at:
            self.expires_at = now() + timedelta(days=365)  # Срок действия 1 год
        super().save(*args, **kwargs)

    def is_valid(self):
        """Проверяет, действителен ли ключ"""
        return self.expires_at and self.expires_at > now()

    def __str__(self):
        return f"{self.user.username} - {self.key} (Действует до {self.expires_at})"


