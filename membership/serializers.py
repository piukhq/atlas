from rest_framework import serializers

from .models import MembershipRequest, MembershipResponse


class MembershipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = '__all__'


class MembershipResponseSerializer(serializers.ModelSerializer):
    payload = serializers.CharField(source="response_body", required=False)

    class Meta:
        model = MembershipResponse
        fields = '__all__'
