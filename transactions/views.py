from __future__ import unicode_literals
from atlas.decorators import token_check
from rest_framework.response import Response
from rest_framework.views import APIView
from transactions.storage import create_blob_from_json
from transactions.serializers import TransactionSerializer
from transactions.models import Transaction

import datetime


class TransactionView(APIView):
    """View to handle incoming transaction data from Aphrodite"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @staticmethod
    @token_check
    def get(request, using_service_token):
        if using_service_token:
            month = request.data['month']
            transactions = Transaction.objects.get(created_date__month=month)
            create_blob_from_json(transactions)

    @token_check
    def post(self, request, using_service_token):
        if using_service_token:
            transaction_data = request.data
            transaction = Transaction(
                created_date=datetime.datetime.now(),
                scheme_provider=transaction_data['scheme_provider'],
                response=transaction_data['response'],
                transaction_id=transaction_data['transaction_id'],
                status=transaction_data['status'],
                transaction_date=transaction_data['transaction_date'],
                user_id=transaction_data['user_id'],
                amount=transaction_data['amount']
            )
            transaction.save()
            return Response(data='Transaction saved', status=201)
        return Response(data='Permission Denied', status=403)
