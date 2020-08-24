from rest_framework import serializers

from .models import MembershipRequest


class MembershipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = '__all__'
