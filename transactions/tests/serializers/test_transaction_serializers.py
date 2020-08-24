from json import dumps
from datetime import datetime
from uuid import uuid1

import pytest

from transactions.serializers import TransactionRequestSerializer
from transactions.tests.factories import TransactionRequestFactory


# ====== Fixtures ======
@pytest.fixture
def transaction_data():
    return {
        "customer_number": 'test_customer_number',
        "membership_plan": 'test_membership_plan',
        "message_uid": str(uuid1()),
        "record_uid": 'test_record_uid',
        "request_timestamp": datetime.now(),
        "response_timestamp": datetime.now(),
        "scheme_provider": 'test_scheme_provider',
        "response": dumps({'test_response_data': 'test_response'}),
        "request": dumps({'test_request_data': 'test_data'}),
        "transaction_id": 'test_transaction_id',
        "status_code": 200,
        "transaction_date": datetime.now(),
        "user_id": 'test_user_id',
        "amount": 1000,
    }


@pytest.fixture
def transaction_object():
    return TransactionRequestFactory()


# ====== Tests ======
@pytest.mark.django_db
def test_transaction_request_valid(transaction_data):
    serializer = TransactionRequestSerializer(data=transaction_data)
    serializer.is_valid(raise_exception=True)

    instance = serializer.save()

    assert instance.customer_number == transaction_data['customer_number']
    assert str(instance.message_uid) == transaction_data['message_uid']


@pytest.mark.django_db
def test_transaction_request_serializer(transaction_object):
    serializer = TransactionRequestSerializer(transaction_object)

    data = serializer.data

    assert data['customer_number'] == transaction_object.customer_number
    assert data['message_uid'] == str(transaction_object.message_uid)
