from json import dumps
from datetime import datetime
from uuid import uuid1

from transactions.models import TransactionRequest
from transactions.save_transactions import store_transaction_data

import pytest


# ====== Fixtures ======
@pytest.fixture
def transaction_body():
    return {
        "scheme_provider": 'test_scheme_provider',
        "message_uid": str(uuid1()),
        "record_uid": 'test_record_uid',
        "response": dumps({'data': 'test_data'}),
        "request": dumps(
            {
                'customer_number': 'test_customer_number',
                'membership_plan': 'test_membership_plan'
            }
        ),
        "transaction_id": 'test_transaction_id',
        "status_code": 200,
        "transaction_date": datetime.now(),
        "user_id": 'test_user_id',
        "amount": 1000,
        "request_timestamp": datetime.now(),
        "response_timestamp": datetime.now(),
    }


# ====== Tests ======
@pytest.mark.django_db
def test_store_transaction_data(transaction_body):
    store_transaction_data(transaction_body)

    transaction = TransactionRequest.objects.get(transaction_id=transaction_body['transaction_id'])

    assert transaction.status_code == transaction_body['status_code']
    assert str(transaction.message_uid) == transaction_body['message_uid']
