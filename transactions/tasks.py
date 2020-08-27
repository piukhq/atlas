from json import loads

from celery.schedules import crontab
from celery.task import periodic_task

from django.conf import settings

from .serializers import TransactionRequestSerializer
from message_queue.queue_agent import MessageQueue


@periodic_task(run_every=crontab(hour=1))
def process_transactions():
    transaction_queue = MessageQueue(settings.TRANSACTION_QUEUE)

    message = transaction_queue.read_message()
    if message:
        request_data = loads(message['request'])
        response_data = loads(message['response'])

        data = message.copy()

        data['customer_number'] = request_data.get('customer_number')
        data['membership_plan'] = request_data.get('membership_plan')
        data['request'] = request_data
        data['response'] = response_data

        serializer = TransactionRequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
