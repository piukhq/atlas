from rest_framework import serializers

from transactions.models import Transaction, TransactionRequest


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        models = TransactionRequest
        fields = '__all__'
