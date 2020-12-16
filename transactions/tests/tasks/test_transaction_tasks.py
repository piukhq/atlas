from datetime import datetime
from json import dumps, loads

import kombu
import pytest

from django.conf import settings

from transactions.models import TransactionRequest
from transactions.tasks import process_transactions


@pytest.fixture
def harvey_nichols_transaction():
    return {
        "scheme_provider": "harvey-nichols",
        "response": {"outcome": "success"},
        "request": {
            "CustomerClaimTransactionRequest": {
                "token": "token",
                "customerNumber": "loyalty-hn-123",
                "id": "d482f186-df55-4da4-bc60-41890bf7a57d"
            }
        },
        "status_code": 200,
        "request_timestamp": "2020-09-02 13:44:14",
        "response_timestamp": "2020-09-02 13:44:14",
        "transactions": [
            {
                "transaction_id": "d482f186-df55-4da4-bc60-41890bf7a57d",
                "user_id": 0,
                "spend_amount": 1099,
                "transaction_date": "2020-05-28 15:46:00"
            }
        ]
    }


@pytest.fixture
def iceland_transactions():
    return {
        "scheme_provider": "iceland-bonus-card",
        "response": "",
        "request": {
            "body": dumps({
                "message_uid": "39dd9217-af99-443a-ab52-fcc248af8d29",
                "transactions": [
                    {
                        "record_uid": "v8vzj4ykl7g28d6mln9x05m31qpeor27",
                        "merchant_scheme_id1": "v8vzj4ykl7g28d6mln9x05m31qpeor27",
                        "merchant_scheme_id2": "test-mid-123",
                        "transaction_id": "75aff1fa-17e9-40e1-bbc9-92f7daffca38"
                    },
                    {
                        "record_uid": "v8vzj4ykl7g28d6mln9x05m31qpeor27",
                        "merchant_scheme_id1": "v8vzj4ykl7g28d6mln9x05m31qpeor27",
                        "merchant_scheme_id2": "test-mid-123",
                        "transaction_id": "11a87408-d4d3-451b-b916-11a4b7c964a1"
                    }
                ]
            })
        },
        "status_code": 200,
        "request_timestamp": "2020-08-27 15:23:13",
        "response_timestamp": "2020-09-02 13:44:14",
        "transactions": [
            {
                "transaction_id": "75aff1fa-17e9-40e1-bbc9-92f7daffca38",
                "user_id": 0,
                "spend_amount": 1099,
                "transaction_date": "2020-06-02 15:46:00"
            },
            {
                "transaction_id": "11a87408-d4d3-451b-b916-11a4b7c964a1",
                "user_id": 0,
                "spend_amount": 1222,
                "transaction_date": "2020-06-02 15:47:45"
            }
        ]
    }



# ====== Tests ======
@pytest.mark.django_db
def test_process_harvey_transactions(harvey_nichols_transaction):
    process_transactions()
    transactions = harvey_nichols_transaction['transactions']
    transaction = TransactionRequest.objects.get(transaction_id=transactions[0]['transaction_id'])

    assert transaction.status_code == harvey_nichols_transaction['status_code']
    assert transaction.response == harvey_nichols_transaction['response']
    assert transaction.customer_number == harvey_nichols_transaction[
        'request']['CustomerClaimTransactionRequest']['customerNumber']


@pytest.mark.django_db
def test_process_iceland_transactions(iceland_transactions):
    process_transactions()
    transactions = TransactionRequest.objects.all()
    request_data = loads(iceland_transactions['request']['body'])['transactions']

    assert len(transactions) == 2

    for num, transaction in enumerate(transactions):
        assert datetime.strftime(transaction.request_timestamp,
                                 '%Y-%m-%d %H:%M:%S') == iceland_transactions['request_timestamp']
        assert transaction.status_code == iceland_transactions['status_code']
        assert transaction.transaction_id == request_data[num]['transaction_id']
        assert transaction.record_uid == request_data[num]['record_uid']
