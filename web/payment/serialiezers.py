# serializers.py
from rest_framework import serializers
from .models import ReadyRequest, ApproveRequest, ReadyResponse

class ReadyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadyRequest
        fields = '__all__'

class ApproveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApproveRequest
        fields = '__all__'

class ReadyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadyResponse
        fields = '__all__'
