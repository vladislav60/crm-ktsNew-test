from rest_framework import serializers
from .models import Alarm


class AlarmSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.username', read_only=True)

    class Meta:
        model = Alarm
        fields = ['id', 'client_name', 'latitude', 'longitude', 'created_at', 'status']