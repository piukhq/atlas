from django.conf import settings

from celery import shared_task

from transactions.merchant import get_merchant
from transactions.serializers import TransactionRequestSerializer
from message_queue.queue_agent import MessageQueue


@shared_task
def process_transactions():
    transaction_queue = MessageQueue(settings.TRANSACTION_QUEUE)
    message = transaction_queue.read_message()

    if message:
        try:
            merchant = get_merchant(message)
            merchant.process_message()

            serializer = TransactionRequestSerializer(data=merchant.audit_list, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except():
            return
