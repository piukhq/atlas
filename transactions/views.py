from __future__ import unicode_literals
from atlas.decorators import token_check
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from transactions.storage import create_blob_from_json
from transactions.serializers import TransactionSerializer
from transactions.models import Transaction
from atlas.settings import logger
import datetime
import json


class TransactionView(APIView):
    """View to handle incoming transaction data from Aphrodite"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @staticmethod
    @token_check
    def get(request, using_service_token):
        if using_service_token:
            start = request.data['start']
            end = request.data['end']
            format_str = '%Y-%m-%d'

            start_datetime = datetime.datetime.strptime(start, format_str)
            end_datetime = datetime.datetime.strptime(end, format_str) + datetime.timedelta(days=1)

            transactions = Transaction.objects.filter(created_date__range=(start_datetime, end_datetime))

            if not transactions:
                return Response(data='No transactions between these dates', status=400)

            serialized_transaction = serializers.serialize('json', transactions)
            scheme_slug = transactions.values('scheme_provider')
            try:
                create_blob_from_json(serialized_transaction, scheme_slug=scheme_slug[0]['scheme_provider'])
            except Exception as e:
                logger.exception(e)

            return Response(data=json.loads(serialized_transaction), status=200)

    @staticmethod
    @token_check
    def post(request, using_service_token):
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
