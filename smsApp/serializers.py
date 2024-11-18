from django.contrib.auth.models import User
from rest_framework import serializers
from .models import SMSStatistic

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    firebase_token = serializers.CharField()
    device_name = serializers.CharField()
    device_id = serializers.CharField()


class SMSStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSStatistic
        fields = ['filed_count', 'success_count']
