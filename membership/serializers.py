from rest_framework import serializers

from .models import MembershipRequest, MembershipResponse


class MembershipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = '__all__'

    def update(self, instance, validated_data):
        # Only update if the value has not already been populated by initial request creation
        for attribute in (
            "address_1", "address_2", "callback_url", "card_number", "channel", "city", "country", "county",
            "email", "first_name", "handler_type", "integration_service", "last_name", "membership_plan_slug",
            "password", "record_uid", "title"
        ):
            instance_attr = getattr(instance, attribute)
            if not instance_attr:
                setattr(instance, attribute, validated_data.get(attribute, instance_attr))

        instance.save()
        return instance


class MembershipResponseSerializer(serializers.ModelSerializer):
    payload = serializers.CharField(source="response_body", required=False)

    class Meta:
        model = MembershipResponse
        fields = '__all__'
