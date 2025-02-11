from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.utils.timezone import now
import logging

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Только авторизованные пользователи могут вызывать API
def send_alarm(request):
    """
    Клиент отправляет тревожный сигнал с координатами.
    """
    data = request.data
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not latitude or not longitude:
        return Response({'error': 'Координаты обязательны'}, status=400)

    alarm = Alarm.objects.create(
        client=request.user,
        latitude=latitude,
        longitude=longitude
    )

    return Response({'success': 'Тревога отправлена', 'alarm_id': alarm.id}, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_alarms(request):
    """
    Оператор получает список активных тревог.
    """
    alarms = Alarm.objects.filter(status__in=['pending', 'in_progress']).order_by('-created_at')
    serializer = AlarmSerializer(alarms, many=True)
    return Response(serializer.data)


@login_required
def panic_map_view(request):
    return render(request, 'panicbutton/map.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'user_api_token': request.user.auth_token.key
    })


from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Alarm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_alarm(request):
    """
    API для создания тревоги клиентом.
    """
    try:
        data = request.data
        print("🔍 Полученные данные:", data)  # ЛОГИРУЕМ ПОЛУЧЕННЫЕ ДАННЫЕ

        client_name = request.user  # Получаем имя пользователя
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not latitude or not longitude:
            return Response({"error": "Необходимо указать координаты"}, status=400)

        # Создаем тревогу
        alarm = Alarm.objects.create(
            client=client_name,
            latitude=float(latitude),
            longitude=float(longitude),
            created_at=now(),
            status="pending"
        )

        # Отправляем WebSocket-сообщение всем операторам
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "alarms",
            {
                "type": "send_alarm",
                "message": {
                    "id": alarm.id,
                    "client_name": alarm.client.username,
                    "latitude": alarm.latitude,
                    "longitude": alarm.longitude,
                    "created_at": alarm.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": alarm.status
                }
            }
        )

        return Response({"success": True, "alarm_id": alarm.id}, status=201)

    except Exception as e:
        print(f"❌ Ошибка в create_alarm: {str(e)}")
        return Response({"error": f"Ошибка сервера: {str(e)}"}, status=500)