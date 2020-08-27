from datetime import datetime
from json import dumps
from uuid import uuid1

import kombu
import pytest

from django.conf import settings

from transactions.models import TransactionRequest
from transactions.tasks import process_transactions


# ====== Fixtures ======
@pytest.fixture
def rabbit_settings(settings):
    settings.RABBITMQ_DSN = 'memory://'


@pytest.fixture
def queue_message():
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


@pytest.fixture
def add_message_to_queue(rabbit_settings, queue_message):
    with kombu.Connection(settings.RABBITMQ_DSN) as conn:
        simple_queue = conn.SimpleQueue(settings.TRANSACTION_QUEUE)
        simple_queue.put(queue_message)
        simple_queue.close()


# ====== Tests ======
@pytest.mark.django_db
def test_process_transactions(rabbit_settings, add_message_to_queue, queue_message):
    process_transactions()
    transaction = TransactionRequest.objects.get(transaction_id=queue_message['transaction_id'])

    assert transaction.status_code == queue_message['status_code']
    assert str(transaction.message_uid) == queue_message['message_uid']
