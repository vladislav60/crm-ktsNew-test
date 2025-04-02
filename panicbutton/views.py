from channels.db import database_sync_to_async
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .models import *
from .serializers import *
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.utils.timezone import now
import logging
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Alarm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import APIKey
from datetime import datetime


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
    alarms = Alarm.objects.filter(status__in=['new', 'pending', 'in_progress']).order_by('-created_at')
    alarms_data = []

    for alarm in alarms:
        alarm_data = AlarmSerializer(alarm).data

        # Загружаем профиль клиента, если есть
        client_profile = ClientProfile.objects.filter(user=alarm.client).first()
        alarm_data["client_profile"] = ClientProfileSerializer(client_profile).data if client_profile else None

        alarms_data.append(alarm_data)

    return Response(alarms_data)


@login_required
def panic_map_view(request):
    return render(request, 'panicbutton/map.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'user_api_token': request.user.apikey.key
    })


@login_required
def test_panic_map_view(request):
    return render(request, 'panicbutton/testmap.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'user_api_token': request.user.apikey.key
    })


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
            created_at=now()
        )

        # Отправляем WebSocket-сообщение всем операторам
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "alarms",
            {
                "type": "send_alarm",
                "message": {
                    "id": alarm.id,
                    "client_id": alarm.client.id,  # now sending client_id
                    "client_name": alarm.client.username,  # you can still send the username if needed
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



@login_required
def get_api_key(request):
    """ Получение текущего API-ключа """
    try:
        api_key = APIKey.objects.get(client__user=request.user)
        return JsonResponse({
            "key": api_key.key,
            "expires_at": api_key.expires_at,
            "is_active": api_key.is_active
        })
    except APIKey.DoesNotExist:
        return JsonResponse({"error": "API-ключ не найден"}, status=404)


@login_required
def request_new_key(request):
    """ Запрос на обновление API-ключа """
    try:
        api_key = APIKey.objects.get(client__user=request.user)
        if api_key.is_active and api_key.expires_at > datetime.now():
            return JsonResponse({"error": "Ваш ключ еще активен"}, status=400)

        # Генерируем новый ключ
        api_key.key = secrets.token_urlsafe(32)
        api_key.expires_at = datetime.now() + timedelta(days=30)
        api_key.is_active = True
        api_key.save()

        return JsonResponse({"message": "API-ключ обновлен", "new_key": api_key.key})
    except APIKey.DoesNotExist:
        return JsonResponse({"error": "API-ключ не найден"}, status=404)



@api_view(['POST'])
@permission_classes([IsAdminUser])  # Только администратор может менять ключи
def update_api_key(request, user_id):
    api_key, created = APIKey.objects.get_or_create(user_id=user_id)

    api_key.key = secrets.token_urlsafe(32)  # Генерация нового ключа
    api_key.expires_at = now() + timedelta(days=365)  # Обновляем срок
    api_key.save()

    return Response({"message": "API-ключ обновлен", "new_key": api_key.key})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def revoke_api_key(request, user_id):
    APIKey.objects.filter(user_id=user_id).delete()
    return Response({"message": "API-ключ аннулирован"})


@login_required
def alarms_view(request):
    return render(request, 'panicbutton/alarms.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'user_api_token': request.user.apikey.key
    })


def get_clients(request):
    clients = ClientProfile.objects.all().values(
        'user_id', 'user__username', 'name_client','description',
        'floor_total','arrival_time','address', 'object_type',
        'route_info', 'floor', 'phone_number', 'contract',
        'last_alarm_at', 'technical_spec', 'intercom_code', 'ekipaz_panic',
    )
    return JsonResponse(list(clients), safe=False)  # Отправляем JSON


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_client(request, client_id):
    client = get_object_or_404(ClientProfile, user_id=client_id)
    data = {
        'user_id': client.user_id,
        'user__username': client.user.username,
        'name_client': client.name_client,
        'description': client.description,
        'floor_total': client.floor_total,
        'arrival_time': client.arrival_time,
        'address': client.address,
        'object_type': client.object_type,
        'route_info': client.route_info,
        'floor': client.floor,
        'phone_number': client.phone_number,
        'contract': client.contract,
        'last_alarm_at': client.last_alarm_at.strftime("%Y-%m-%d %H:%M:%S") if client.last_alarm_at else None,
        'technical_spec': client.technical_spec,
        'intercom_code': client.intercom_code,
        'ekipaz_panic': client.ekipaz_panic,
    }
    return Response(data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_client(request, client_id):
#     client = get_object_or_404(ClientProfile, user_id=client_id)
#     serializer = ClientProfileSerializer(client)
#     return Response(serializer.data)

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import AlarmSerializer


@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_alarm_status(request, alarm_id):
    data = json.loads(request.body)
    new_status = data.get("status")

    try:
        alarm = Alarm.objects.get(id=alarm_id)
        alarm.status = new_status
        alarm.save()

        # Отправка обновлённой информации по WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "alarms",
            {
                "type": "send_alarm",
                "message": AlarmSerializer(alarm).data
            }
        )

        return JsonResponse({"success": True, "new_status": alarm.status})
    except Alarm.DoesNotExist:
        return JsonResponse({"error": "Alarm not found"}, status=404)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def login_with_api_key(request):
    """
    Эндпоинт аутентификации по API ключу.
    Принимает JSON с полем "api_key".
    Если ключ действительный, возвращает статус 200 и сообщение об успехе.
    """
    api_key = request.data.get("api_key")
    if not api_key:
        return Response({"error": "API ключ не предоставлен"}, status=status.HTTP_400_BAD_REQUEST)

    from .models import APIKey  # Импорт модели APIKey
    key_instance = APIKey.objects.filter(key=api_key).first()

    if key_instance and key_instance.is_valid():
        return Response({"message": "Аутентификация успешна"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Неверный или недействительный API ключ"}, status=status.HTTP_401_UNAUTHORIZED)

