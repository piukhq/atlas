from rest_framework import serializers

from transactions.models import AuditData, ExportTransaction, Transaction, TransactionRequest


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


class ExportTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportTransaction
        fields = ["loyalty_identifier", "transaction_id", "transaction_date", "user_id", "spend_amount", "record_uid"]


class AuditDataSerializer(serializers.Serializer):
    provider_slug = serializers.CharField(max_length=250)
    transactions = ExportTransactionSerializer(many=True)
    audit_data = serializers.JSONField(required=False)

    def create(self, validated_data):
        transactions = validated_data.pop("transactions")
        audit_data = AuditData.objects.create(audit_data=validated_data["audit_data"])
        for transaction_data in transactions:
            transaction_data["provider_slug"] = validated_data["provider_slug"]
            ExportTransaction.objects.create(audit_data=audit_data, **transaction_data)
        return audit_data

