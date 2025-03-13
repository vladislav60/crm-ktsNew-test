from rest_framework import serializers
from .models import *


class AlarmSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(source='client.id', read_only=True)
    client_name = serializers.CharField(source='client.username', read_only=True)

    class Meta:
        model = Alarm
        fields = ['id', 'client_name', 'client_id', 'latitude', 'longitude', 'created_at', 'status']


class ClientProfileSerializer(serializers.ModelSerializer):
    last_alarm_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True)

    class Meta:
        model = ClientProfile
        fields = ['user', 'phone_number', 'address', 'last_alarm_at']