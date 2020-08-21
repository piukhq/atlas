from rest_framework import serializers

from .models import EnrolRequest


class EnrolRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrolRequest
        fields = '__all__'
