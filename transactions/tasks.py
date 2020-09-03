from json import loads

from celery.schedules import crontab
from celery.task import periodic_task

from django.conf import settings

from transactions.serializers import TransactionRequestSerializer
from message_queue.queue_agent import MessageQueue


@periodic_task(run_every=crontab(hour=1))
def process_transactions():
    transaction_queue = MessageQueue(settings.TRANSACTION_QUEUE)
    message = transaction_queue.read_message()

    if message:
        audit_data = []
        request = message['request']

        data = {
            'status_code': message['status_code'],
            'message_uid': request.get('message_uid', ""),
            'request_timestamp': message['request_timestamp'],
            'response_timestamp': message['response_timestamp'],
            'request': request,
            'response': message['response'],
            'membership_plan': message['scheme_provider']
        }

        # customer number provided for Harvey Nichols
        if request.get('CustomerClaimTransactionRequest'):
            data['customer_number'] = request['CustomerClaimTransactionRequest']['customerNumber']

        # Iceland provides a list of transactions, so we need to loop through and bulk create.
        if request.get('body'):
            data['message_uid'] = loads(request['body']).get('message_uid')
            transactions = loads(request['body'])['transactions']

            if isinstance(transactions, list):
                for transaction in transactions:
                    transaction_data = data.copy()
                    transaction_data['transaction_id'] = transaction['transaction_id']
                    transaction_data['record_uid'] = transaction['record_uid']
                    audit_data.append(transaction_data)
        else:
            data['transaction_id'] = message['transactions'][0]['transaction_id']
            audit_data.append(data)

        serializer = TransactionRequestSerializer(data=audit_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
