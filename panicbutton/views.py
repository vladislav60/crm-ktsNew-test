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