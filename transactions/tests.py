from django.core import serializers
from django.test import TestCase, Client
from unittest.mock import patch

# patch('atlas.decorators.token_check', lambda x: x).start()
from transactions.views import get_transactions, save_transaction
from transactions.models import Transaction
from requests import request
from django.http import HttpRequest
from rest_framework.response import Response
import datetime
import json
from atlas.settings import ATLAS_SERVICE_AUTH_HEADER as key


class TestCreateTransactionInDB(TestCase):

    def setUp(self):
        self.auth_headers = {'HTTP_AUTHORIZATION': key}
        self.data = {'start': "2018-12-09", "end": "2018-12-11"}

        self.valid_payload = {
            'scheme_provider': 'harvey-nichols',
            'status': 'SUCCESS',
            'transaction_id': '12',
            'response': '{key: value}',
            'transaction_date': datetime.datetime.now(),
            'user_id': '11111',
            'amount': 12.0
        }

        self.invalid_payload = {
            'created_date': "2018-12-08",
            'scheme_provider': 'harvey-nichols',
            'status': 'SUCCESS',
            'transaction_id': '123456789',
            'response': '{key: value}',
            'transaction_date': datetime.datetime.now(),
            'user_id': '11111',
            'amount': 12.0
        }

    def test_empty_list_returned_if_no_transaction_between_dates(self):
        transaction_item_one = Transaction.objects.create(
            created_date=datetime.datetime.now(),
            scheme_provider='harvey-nichols',
            status='SUCCESS',
            transaction_id='1',
            response='{key: value}',
            transaction_date=datetime.datetime.now(),
            user_id='1234',
            amount=12.0
        )
        transaction_item_one.save()

        resp = get_transactions("2018-12-07", "2018-12-08")
        result = json.loads(resp)
        self.assertEqual(result, [])

    def test_transaction_returned_between_dates(self):
        transaction_item_one = Transaction.objects.create(
            created_date=datetime.datetime.now(),
            scheme_provider='harvey-nichols',
            status='SUCCESS',
            transaction_id='1',
            response='{key: value}',
            transaction_date=datetime.datetime.now(),
            user_id='1234',
            amount=12.0
        )
        transaction_item_one.save()

        resp = get_transactions("2018-12-10", str(datetime.date.today()))
        result = json.loads(resp)
        self.assertEqual(len(result), 1)

    def test_create_valid_transaction(self):
        response = save_transaction(self.valid_payload)
        self.assertEqual(response.status_code, 201)

    @patch('transactions.storage.create_blob_from_json')
    def test_auth_decorator_passes_when_token_is_used(self, mock_blob):
        mock_blob.return_value = 'test'
        transaction_item_one = Transaction.objects.create(
            created_date=datetime.datetime.now(),
            scheme_provider='harvey-nichols',
            status='SUCCESS',
            transaction_id='1',
            response='{key: value}',
            transaction_date=datetime.datetime.now(),
            user_id='1234',
            amount=12.0
        )
        transaction_item_one.save()

        resp = self.client.post('/transaction/blob', self.data, **self.auth_headers)
        self.assertEqual(resp.status_code, 200)

    def test_auth_decorator_raises_exception_when_not_used(self):

        resp = self.client.post('/transaction/blob', self.data)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.exception, True)
