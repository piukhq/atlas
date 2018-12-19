from __future__ import unicode_literals

import datetime
import json

from azure.common import AzureException
from django.core import serializers
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView

from atlas.decorators import token_check
from atlas.settings import logger
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from transactions.storage import create_blob_from_json


class TransactionBlobView(APIView):
    """View to query Transaction database and save result to blob storage"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @staticmethod
    @token_check
    def post(request):

        start = request.data['start']
        end = request.data['end']

        try:
            transactions = get_transactions(start, end)

        except (ValueError, TypeError) as e:
            logger.exception(
                'TransactionBlobView: Date must reflect YYYY-MM-DD format: {}'.format(e.args[0]))
            return Response(data='Date must reflect YYYY-MM-DD format: {}'.format(e.args[0]), status=400)

        trans = json.loads(transactions)

        if not trans:
            logger.info('TransactionBlobView: No transactions between these dates: {}--{}'.format(start, end))
            return Response(data='No transactions between these dates: {}--{}'.format(start, end), status=204)

        try:
            create_blob_from_json(transactions, scheme_slug=trans[0]['fields']['scheme_provider'])

        except AzureException as e:
            logger.exception('TransactionBlobView: Error saving to Blob storage - {} data - {}'.format(e, trans))
            return Response(
                data='Error saving to blob storage - {} data - {}'.format(e, trans),
                status=e.status_code)

        except ValueError as e:
            logger.exception(
                'TransactionBlobView: Error saving to Blob storage - {} data - {}'.format(e.args[0], trans))
            return Response(
                data='Error saving to blob storage - {} data - {}'.format(e.args[0], trans),
                status=520)

        return Response(data=trans, status=200)


class TransactionSaveView(APIView):
    """View to handle incoming transaction data from Aphrodite and save to postgres"""

    @staticmethod
    @token_check
    def post(request):
        try:
            transaction = save_transaction(request.data)
            return transaction

        except (IntegrityError, KeyError, Exception) as e:
            logger.exception('Error saving transaction: {}'.format(e.args[0]))
            return Response(data="Transaction not saved: {}".format(e.args[0]), status=400)


def get_transactions(start_date, end_date):
    format_str = '%Y-%m-%d'

    start_datetime = datetime.datetime.strptime(start_date, format_str)
    end_datetime = datetime.datetime.strptime(end_date, format_str) + datetime.timedelta(days=1)

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
    return Response(data='Transaction saved: {}'.format(transaction), status=201)
