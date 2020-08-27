from uuid import uuid4
from datetime import datetime

import factory

from transactions.models import TransactionRequest


class TransactionRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransactionRequest

    customer_number = 'test_card_number_1234'
    transaction_id = 'test_transaction_id'
    request_timestamp = datetime.now()
    membership_plan = 'test_membership_plan'
    message_uid = uuid4()
    record_uid = 'test_bink_record_id'
    request = {'data': 'test_data'}
    status_code = 200
    response = {'data': 'test_response_data'}
    response_timestamp = datetime.now()
