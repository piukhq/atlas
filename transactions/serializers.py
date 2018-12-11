from rest_framework import serializers

from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(input_formats=["%Y/%M/%D %H/%M/%S"], required=True)
    scheme_provider = serializers.CharField(max_length=100, read_only=True)
    response = serializers.CharField(max_length=3000, read_only=True)
    transaction_id = serializers.CharField(max_length=100, read_only=True)
    status = serializers.CharField(max_length=50, read_only=True)
    transaction_date = serializers.DateTimeField(input_formats=["%Y/%M/%D %H/%M/%S"], read_only=True)
    user_id = serializers.CharField(max_length=30, read_only=True)
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = Transaction
        fields = ('created_date', 'scheme_provider', 'response', 'transaction_id', 'status', 'transaction_date',
                  'user_id', 'amount')
