from uuid import uuid1

import pytest

from transactions.serializers import TransactionRequestSerializer
from transactions.tests.factories import TransactionRequestFactory


# ====== Fixtures ======
@pytest.fixture
def transaction_data():
    return [
        {
            "status_code": 200,
            "message_uid": str(uuid1()),
            "request_timestamp": "2020-09-02 13:44:14",
            "response_timestamp": "2020-09-02 13:44:14",
            "request": {
                "CustomerClaimTransactionRequest": {
                    "token": "token",
                    "customerNumber": "loyalty-hn-123",
                    "id": "d482f186-df55-4da4-bc60-41890bf7a57d",
                }
            },
            "response": {"outcome": "success"},
            "membership_plan": "harvey-nichols",
            "customer_number": "loyalty-hn-123",
            "transaction_id": "d482f186-df55-4da4-bc60-41890bf7a57d",
        }
    ]


@pytest.fixture
def transaction_object():
    return TransactionRequestFactory()


# ====== Tests ======
@pytest.mark.django_db
def test_transaction_request_valid(transaction_data):
    serializer = TransactionRequestSerializer(data=transaction_data, many=True)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()

    assert len(instance) == 1
    assert instance[0].customer_number == transaction_data[0]["customer_number"]
    assert instance[0].membership_plan == transaction_data[0]["membership_plan"]
    assert instance[0].status_code == transaction_data[0]["status_code"]
    assert instance[0].message_uid == transaction_data[0]["message_uid"]


@pytest.mark.django_db
def test_transaction_request_serializer(transaction_object):
    serializer = TransactionRequestSerializer(transaction_object)

    data = serializer.data

    assert data["customer_number"] == transaction_object.customer_number
    assert data["message_uid"] == str(transaction_object.message_uid)
