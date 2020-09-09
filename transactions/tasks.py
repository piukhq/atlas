from celery.schedules import crontab
from celery.task import periodic_task

from django.conf import settings

from transactions.merchant import get_merchant
from transactions.serializers import TransactionRequestSerializer
from message_queue.queue_agent import MessageQueue


@periodic_task(run_every=crontab(
    minute=settings.CRONTAB_MINUTES,
    hour=f'*/{settings.CRONTAB_HOUR}')
)
def process_transactions():
    transaction_queue = MessageQueue(settings.TRANSACTION_QUEUE)
    message = transaction_queue.read_message()

    if message:
        merchant = get_merchant(message)
        merchant.process_message()

        serializer = TransactionRequestSerializer(data=merchant.audit_list, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
