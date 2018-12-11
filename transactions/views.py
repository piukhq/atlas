from __future__ import unicode_literals

import datetime
import json

from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from atlas.decorators import token_check
from atlas.settings import logger
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from transactions.storage import create_blob_from_json


class TransactionBlobView(APIView):
    """View to handle incoming transaction data from Aphrodite"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @staticmethod
    @token_check
    def post(request):

        start = request.data['start']
        end = request.data['end']

        transactions = get_transactions(start, end)

        if not transactions:
            return Response(data='No transactions between these dates', status=400)

        trans = json.loads(transactions)

        try:
            create_blob_from_json(transactions, scheme_slug=trans[0]['fields']['scheme_provider'])
        except Exception as e:
            logger.exception(e)
            return Response(data=transactions, status=500)

        return Response(data=transactions, status=200)


class TransactionSaveView(APIView):

    @staticmethod
    @token_check
    def post(request):
        return save_transaction(request.data)


def get_transactions(start_date, end_date):
    format_str = '%Y-%m-%d'

    try:
        start_datetime = datetime.datetime.strptime(start_date, format_str)
        end_datetime = datetime.datetime.strptime(end_date, format_str) + datetime.timedelta(days=1)

    except ValueError:
        logger.exception(ValueError)
        return Response(data='Date must reflect YYYY-MM-DD format', status=400)

    transactions = Transaction.objects.filter(created_date__range=(start_datetime, end_datetime))
    serialized_transaction = serializers.serialize('json', transactions)
    return serialized_transaction


def save_transaction(transaction_data):
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

