import datetime
from unittest import mock
from unittest.mock import patch

import kombu
from atlas.settings import ATLAS_SERVICE_AUTH_HEADER
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from transactions.models import AuditData, Transaction
from transactions.serializers import AuditDataSerializer
from transactions.tasks import process_transaction
from transactions.views import get_transactions


class TestGetTransactions(TestCase):

    def setUp(self):
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
        self.transaction_item_diff_slug = Transaction.objects.create(
            created_date=datetime.datetime.now(),
            scheme_provider='iceland',
            status='SUCCESS',
            transaction_id='2',
            response='{key: value}',
            transaction_date=datetime.datetime.now(),
            user_id='1234',
            amount=12.0
        )
        self.transaction_item.refresh_from_db()

    def test_empty_list_returned_if_no_transaction_between_dates(self):
        self.transaction_item.save()

        resp = get_transactions("2018-12-07", "2018-12-08", "harvey-nichols")
        self.assertEqual(resp, [])

    def test_wrong_date_format_throws_error(self):
        self.assertRaises(ValueError, lambda: get_transactions("07-12-2018", "08-12-2018", "harvey-nichols"))

    def test_correct_transaction_returned(self):
        self.transaction_item.save()
        self.transaction_item_diff_slug.save()

        resp = get_transactions("2018-12-10", str(datetime.date.today()), "harvey-nichols")
        self.assertEqual(len(resp), 1)
        self.assertEqual(resp[0]['scheme_provider'], "harvey-nichols")

        resp = get_transactions("2018-12-10", str(datetime.date.today()), "iceland")
        self.assertEqual(len(resp), 1)
        self.assertEqual(resp[0]['scheme_provider'], "iceland")


class TestTransactionBlobView(APITestCase):

    def setUp(self):
        self.auth_headers = ATLAS_SERVICE_AUTH_HEADER
        self.url = reverse('transaction_blob_storage')
        self.data = {'start': "2018-12-09", "end": "2018-12-10", "scheme_slug": "harvey-nichols"}
        self.end_date_before_start_data = {'start': "2018-12-12", "end": "2018-12-10", "scheme_slug": "harvey-nichols"}
        self.bad_date_format_data = {'start': "09-01-2019", "end": "12-01-2019", "scheme_slug": "harvey-nichols"}
        self.transaction_object = Transaction.objects.create(
            created_date=datetime.datetime.now(),
            scheme_provider='harvey-nichols',
            status='SUCCESS',
            transaction_id='2',
            response='{key: value}',
            transaction_date=datetime.datetime.now(),
            user_id='1234',
            amount=12.0
        )
        self.transaction_object.refresh_from_db()

    @patch('transactions.views.write_to_csv')
    @patch('transactions.views.create_blob_from_csv')
    @patch('transactions.views.get_transactions')
    def test_get_transaction_is_called_if_dates_are_correct_format(self, mock_get_transactions,
                                                                   mock_create_blob, mock_write_to_csv):
        mock_get_transactions.return_value = [{
            'created_date': datetime.datetime.now(),
            'scheme_provider': 'harvey-nichols',
            'response': 'SUCCESS',
            'transaction_id': '2',
            'status': '{key: value}',
            'transaction_date': datetime.datetime.now(),
            'user_id': '1234',
            'amount': 12.0
        }]
        self.transaction_object.save()
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        self.client.post(self.url, self.data, format='json')
        mock_get_transactions.assert_called_with("2018-12-09", "2018-12-10", 'harvey-nichols')

    def test_bad_request_if_end_date_precedes_start_date(self):
        self.transaction_object.save()
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.post(self.url, self.end_date_before_start_data, format='json')

        self.assertEqual(resp.data, 'Date Error: start date must precede end date')
        self.assertEqual(resp.status_code, 400)

    @patch('transactions.views.get_transactions')
    def test_incorrect_date_format_throws_error(self, mock_get_transactions):
        mock_get_transactions.side_effect = ValueError(mock.Mock)
        self.transaction_object.save()
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.post(self.url, self.bad_date_format_data, format='json')
        self.assertTrue(type(resp.data) is str)
        self.assertEqual(resp.status_code, 400)

    @patch('transactions.views.get_transactions')
    def test_no_transactions_between_dates_returns_correct_error_message(self, mock_get_transactions):
        mock_get_transactions.return_value = []
        self.transaction_object.save()
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.post(self.url, self.data, format='json')
        self.assertEqual(resp.data, 'No transactions exist between these dates: 2018-12-09--2018-12-10')
        self.assertEqual(resp.status_code, 204)

    @patch('transactions.views.get_transactions')
    @patch('transactions.views.create_blob_from_csv')
    def test_azure_exception_error_message(self, mock_create_blob_from_csv, mock_get_transactions):
        mock_get_transactions.return_value = [{
            'created_date': datetime.datetime.now(),
            'scheme_provider': 'harvey-nichols',
            'response': 'SUCCESS',
            'transaction_id': '2',
            'status': '{key: value}',
            'transaction_date': datetime.datetime.now(),
            'user_id': '1234',
            'amount': 12.0
        }]
        mock_create_blob_from_csv.side_effect = Exception(mock.Mock(status=status.HTTP_500_INTERNAL_SERVER_ERROR))
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.post(self.url, self.data, format='json')
        self.assertTrue(type(resp.data) is str)
        self.assertEqual(resp.status_code, 500)

    @patch('transactions.views.get_transactions')
    @patch('transactions.views.create_blob_from_csv')
    def test_200_ok_response_for_valid_data(self, mock_create_blob_from_csv, mock_get_transactions):
        mock_get_transactions.return_value = [{
            'created_date': datetime.datetime.now(),
            'scheme_provider': 'harvey-nichols',
            'response': 'SUCCESS',
            'transaction_id': '2',
            'status': '{key: value}',
            'transaction_date': datetime.datetime.now(),
            'user_id': '1234',
            'amount': 12.0
        }]
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.post(self.url, self.data, format='json')
        self.assertTrue(type(resp.data) is list)
        self.assertEqual(resp.status_code, 200)


class TestSaveEndpoint(APITestCase):

    def setUp(self):
        self.auth_headers = ATLAS_SERVICE_AUTH_HEADER
        self.url = reverse('postgres')

        self.payload = {
            'scheme_provider': 'harvey-nichols',
            'status': 'SUCCESS',
            'transaction_id': '12',
            'response': '{key: value}',
            'transaction_date': datetime.datetime.now(),
            'user_id': '11111',
            'amount': 12.0
        }

        self.bad_payload = {
            'status': 'SUCCESS',
            'transaction_id': '12',
            'response': '{key: value}',
            'transaction_date': datetime.datetime.now(),
            'user_id': '11111',
            'amount': 12.0
        }

    def test_persist_valid_transaction(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().scheme_provider, 'harvey-nichols')

    def test_auth_decorator_passes_when_token_is_used(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.post(self.url, self.bad_payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_duplicate_transaction_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.count(), 1)


class TestExportTransaction(APITestCase):

    # MER-645: the new-style transaction data from Harmonia
    def setUp(self):
        self.export_transaction_data = {
            "provider_slug": "iceland-bonus-card",
            "transactions": [
                {
                    "transaction_id": 1,
                    "user_id": 0,
                    "spend_amount": 1222,
                    "transaction_date": "2020-10-27 15:01:00",
                    "loyalty_identifier": "88899966",
                    "record_uid": None,
                },
                {
                    "transaction_id": 2,
                    "user_id": 0,
                    "spend_amount": 1222,
                    "transaction_date": "2020-10-27 15:01:00",
                    "loyalty_identifier": "99999999",
                    "record_uid": "a544642d-012f-45cd-88c6-a436df62924f",
                },
            ],
            "audit_data": {
                "request": {
                    "body": ('{"message_uid": "e0dc4d6b-1184-4b70-909b-b2472efae96a", "transactions": '
                             '[{"record_uid": "v8vzj4ykl7g28d6mln9x05m31qpeor27", "merchant_scheme_id1": '
                             '"v8vzj4ykl7g28d6mln9x05m31qpeor27", "merchant_scheme_id2": "88899966", '
                             '"transaction_id": "a544642d-012f-45cd-88c6-a436df62924f"}]}'),
                    "timestamp": "2021-01-18 14:46:14",
                },
                "response": {"body": "", "status_code": 200, "timestamp": "2021-01-18 14:46:14"},
            },
        }

    def test_auditdata_request_is_valid(self):
        audit_data_serializer = AuditDataSerializer(data=self.export_transaction_data)
        audit_data_serializer.is_valid(raise_exception=True)
        instance = audit_data_serializer.save()

        assert instance.audit_data["request"] == self.export_transaction_data["audit_data"]["request"]
        assert instance.audit_data["response"] == self.export_transaction_data["audit_data"]["response"]
        export_transactions = instance.exporttransaction_set.all()
        assert export_transactions[0].loyalty_identifier == "88899966"
        assert export_transactions[0].provider_slug == "iceland-bonus-card"
        assert export_transactions[1].loyalty_identifier == "99999999"
        assert export_transactions[1].provider_slug == "iceland-bonus-card"


class TestTransactionTask(APITestCase):

    # MER-645: the new-style transaction data from Harmonia
    def setUp(self):
        settings.AMQP_DSN = 'memory://'
        self.export_transaction_data = {
            "provider_slug": "iceland-bonus-card",
            "transactions": [
                {
                    "transaction_id": 1,
                    "user_id": 0,
                    "spend_amount": 1222,
                    "transaction_date": "2020-10-27 15:01:00",
                    "loyalty_identifier": "88899966",
                    "record_uid": None,
                },
                {
                    "transaction_id": 2,
                    "user_id": 0,
                    "spend_amount": 1222,
                    "transaction_date": "2020-10-27 15:01:00",
                    "loyalty_identifier": "99999999",
                    "record_uid": "a544642d-012f-45cd-88c6-a436df62924f",
                },
            ],
            "audit_data": {
                "request": {
                    "body": ('{"message_uid": "e0dc4d6b-1184-4b70-909b-b2472efae96a", "transactions": '
                             '[{"record_uid": "v8vzj4ykl7g28d6mln9x05m31qpeor27", "merchant_scheme_id1": '
                             '"v8vzj4ykl7g28d6mln9x05m31qpeor27", "merchant_scheme_id2": "88899966", '
                             '"transaction_id": "a544642d-012f-45cd-88c6-a436df62924f"}]}'),
                    "timestamp": "2021-01-18 14:46:14",
                },
                "response": {"body": "", "status_code": 200, "timestamp": "2021-01-18 14:46:14"},
            },
        }

    def test_transaction_task(self):
        with kombu.Connection(settings.AMQP_DSN) as conn:
            simple_queue = conn.SimpleQueue(settings.TRANSACTION_QUEUE)
            simple_queue.put(self.export_transaction_data)
            simple_queue.close()

        with kombu.Connection(settings.AMQP_DSN) as conn:
            simple_queue = conn.SimpleQueue(settings.TRANSACTION_QUEUE)
            transaction_message = simple_queue.get().payload
            simple_queue.close()

        process_transaction(transaction_message)
        transactions = AuditData.objects.all()

        assert transactions[0]
        assert transactions[0].audit_data["request"] == self.export_transaction_data["audit_data"]["request"]
        assert transactions[0].audit_data["response"] == self.export_transaction_data["audit_data"]["response"]
        export_transactions = transactions[0].exporttransaction_set.all()
        assert export_transactions[0].loyalty_identifier == "88899966"
        assert export_transactions[0].provider_slug == "iceland-bonus-card"
        assert export_transactions[1].loyalty_identifier == "99999999"
        assert export_transactions[1].provider_slug == "iceland-bonus-card"
