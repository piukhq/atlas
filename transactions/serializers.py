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
        fields = '__all__'

        # created_date = models.DateTimeField(auto_now_add=True, db_index=True, blank=False)
        # provider_slug = models.CharField(max_length=100, db_index=True)
        # loyalty_identifier = models.CharField(max_length=250, blank=True, db_index=True)
        # transaction_id = models.CharField(max_length=100, db_index=True, unique=True)
        # transaction_date = models.DateTimeField(blank=True, db_index=True)
        # user_id = models.CharField(max_length=30, blank=True)
        # data = models.ForeignKey(AuditData, on_delete=models.CASCADE)
        # record_uid = models.CharField(max_length=500, blank=True)


class AuditDataSerializer(serializers.ModelSerializer):
    export_transaction = ExportTransactionSerializer()

    class Meta:
        model = AuditData
        fields = ["provider_slug", "transactions", "audit_data", "export_transaction"]

    def validate(self, data):
        return data

    def create(self, validated_data):
        transactions = validated_data.pop("transactions")
        audit_data = AuditData.objects.create(**validated_data)
        for transaction_data in transactions:
            transaction_data["provider_slug"] = validated_data["provider_slug"]
            ExportTransaction.objects.create(data=audit_data, **transaction_data)
        return audit_data

    provider_slug = serializers.CharField(max_length=250)
    transactions = ExportTransactionSerializer(many=True)
    audit_data = serializers.JSONField(required=False)
