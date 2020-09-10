from rest_framework import serializers

from transactions.models import Transaction, TransactionRequest


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionRequestListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        transaction_requests = [TransactionRequest(**item) for item in validated_data]
        return TransactionRequest.objects.bulk_create(transaction_requests)


class TransactionRequestSerializer(serializers.Serializer):
    customer_number = serializers.CharField(max_length=250, required=False, allow_blank=True)
    transaction_id = serializers.CharField(max_length=250, required=False, allow_blank=True)
    request_timestamp = serializers.DateTimeField(required=False)
    response_timestamp = serializers.DateTimeField(required=False)
    membership_plan = serializers.CharField(required=False, allow_blank=True, max_length=64)
    message_uid = serializers.CharField(max_length=250, required=False, allow_blank=True)
    record_uid = serializers.CharField(max_length=100, required=False, allow_blank=True)
    request = serializers.JSONField(required=False)
    response = serializers.JSONField(required=False)
    status_code = serializers.IntegerField(required=False)

    class Meta:
        list_serializer_class = TransactionRequestListSerializer
