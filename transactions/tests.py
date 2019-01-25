import datetime
import json

from django.test import TestCase

from atlas.settings import ATLAS_SERVICE_AUTH_HEADER as key
from transactions.models import Transaction
from transactions.views import get_transactions


class TestBlobStorageEndpoint(TestCase):

    def setUp(self):
        self.auth_headers = {'HTTP_AUTHORIZATION': key}
        self.data = {'start': "2018-12-09", "end": datetime.datetime.now()}
        self.transaction_item = Transaction.objects.create(
            created_date=datetime.datetime.now(),
            scheme_provider='harvey-nichols',
            status='SUCCESS',
            transaction_id='1',
            response='{key: value}',
            transaction_date=datetime.datetime.now(),
            user_id='1234',
            amount=12.0
        )
        self.transaction_item.refresh_from_db()

    def test_empty_list_returned_if_no_transaction_between_dates(self):

        self.transaction_item.save()

        resp = get_transactions("2018-12-07", "2018-12-08")
        result = json.loads(resp)
        self.assertEqual(result, [])

    def test_dates_wrong_format(self):

        self.transaction_item.save()

        resp = get_transactions("07-12-2018", "08-12-2018")
        self.assertRaises(ValueError)
        self.assertEqual(resp.status_code, 400)

    def test_transaction_returned_between_dates(self):

        self.transaction_item.save()

        resp = get_transactions("2018-12-10", str(datetime.date.today()))
        result = json.loads(resp)
        self.assertEqual(len(result), 1)

    def test_auth_decorator_raises_exception_when_not_used(self):

        resp = self.client.post('/transaction/blob', self.data)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.exception, True)


class TestSaveEndpoint(TestCase):

    def setUp(self):
        self.auth_headers = {'HTTP_AUTHORIZATION': key}

        self.payload = {
            'scheme_provider': 'harvey-nichols',
            'status': 'SUCCESS',
            'transaction_id': 'test_id',
            'response': '{key: value}',
            'transaction_date': datetime.datetime.now(),
            'user_id': '11111',
            'amount': 12.0
        }

    def test_save_transaction(self):
        transaction = Transaction.objects.filter(transaction_id='test_id')
        self.assertFalse(transaction)

        resp = self.client.post('/transaction/save', self.payload, **self.auth_headers)
        self.assertEqual(resp.status_code, 201)

        new_transaction = Transaction.objects.get(transaction_id='test_id')
        self.assertEqual(new_transaction.status, 'SUCCESS')

    def test_auth_decorator_fails_when_token_is_not_used(self):
        resp = self.client.post('/transaction/save', self.payload)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.exception, True)
