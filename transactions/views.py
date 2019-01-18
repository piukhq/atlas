from __future__ import unicode_literals

import datetime
import json

from azure.common import AzureException
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from atlas.decorators import token_check
from atlas.settings import logger
from atlas.storage import create_blob_from_csv
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer


class TransactionBlobView(APIView):
    """View to query Transaction database and save result to blob storage"""

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

        # TODO change base directory to variable 'merchant' and pass in merchant name
        try:
            create_blob_from_csv(transactions,
                                  file_name=trans[0]['fields']['scheme_provider'],
                                  base_directory='schemes',
                                  container='transaction-reports-test')

        except AzureException as e:
            logger.exception('TransactionBlobView: Error saving to Blob storage - {} data - {}'.format(e, trans))
            return Response(
                data='Error saving to blob storage - {} data - {}'.format(e, trans),
                status=e.status_code)

        except Exception as e:
            logger.exception(
                'TransactionBlobView POST: Error saving to Blob storage - {} data - {}'.format(e, trans))
            return Response(
                data='Error saving to blob storage - {} data - {}'.format(e.args[0], trans),
                status=500)

        return Response(data=trans, status=200)


class TransactionSaveView(APIView):
    """View to handle incoming transaction data from Aphrodite and save to postgres"""

    @staticmethod
    @token_check
    def post(request):
        transaction_serializer = TransactionSerializer(data=request.data)

        if transaction_serializer.is_valid():
            transaction_serializer.save()
            return Response(data='Transaction saved: {}'.format(transaction_serializer.data), status=201)
        logger.warning('TransactionSaveView: Transaction NOT saved {}'.format(transaction_serializer.errors))
        return Response(data='Transaction NOT saved: {}'.format(transaction_serializer.errors), status=400)


def get_transactions(start_date, end_date):
    format_str = '%Y-%m-%d'

    start_datetime = datetime.datetime.strptime(start_date, format_str)
    end_datetime = datetime.datetime.strptime(end_date, format_str) + datetime.timedelta(days=1)

    transactions = Transaction.objects.filter(created_date__range=(start_datetime, end_datetime))
    serialized_transaction = serializers.serialize('json', transactions)
    return serialized_transaction
