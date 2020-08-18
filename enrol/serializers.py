from rest_framework import serializers

from .models import EnrolRequest, EnrolResponse


class EnrolRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrolRequest
        fields = '__all__'


class EnrolResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrolResponse
        fields = '__all__'
