from rest_framework import serializers

from .models import Enrol


class EnrolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrol
        fields = '__all__'
