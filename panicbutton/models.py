from django.db import models
from django.contrib.auth.models import User


class Operator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_operator = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Alarm(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('in_progress', 'В работе'),
        ('resolved', 'Завершено'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время тревоги")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")

    def __str__(self):
        return f"Тревога от {self.client.username} ({self.get_status_display()})"


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Клиент")
    description = models.TextField(blank=True, verbose_name="Описание объекта")
    object_type = models.CharField(max_length=255, blank=True, verbose_name="Тип объекта")
    route_info = models.TextField(blank=True, verbose_name="Текстовое обозначение маршрута")
    floor = models.IntegerField(blank=True, null=True, verbose_name="Этаж")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    contract = models.CharField(max_length=50, blank=True, verbose_name="Договор")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return f"{self.user.username} - {self.address}"
