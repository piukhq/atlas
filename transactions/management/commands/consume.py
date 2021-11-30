import logging

import kombu
import kombu.mixins
from django.conf import settings
from django.core.management.base import BaseCommand

from prometheus.signals import transaction_fail, transaction_success
from transactions import tasks

logger = logging.getLogger(__name__)


class Consumer(kombu.mixins.ConsumerMixin):
    def __init__(self, connection):
        self.queues = [kombu.Queue(settings.TRANSACTION_QUEUE)]
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(self.queues, callbacks=[self.on_message])]

    def on_message(self, body, message):
        logger.info("Received transaction message.")

        try:
            tasks.process_transaction(body)
        except Exception:
            transaction_fail.send(sender="TransactionSaveView.post")
            raise
        else:
            message.ack()
            transaction_success.send(sender="TransactionSaveView.post")


class Command(BaseCommand):
    help = "Consume auth transactions from the specified queue"

    def handle(self, *args, **options):
        logger.info(f"Consuming from queue: {settings.TRANSACTION_QUEUE}")
        conn = kombu.Connection(settings.AMQP_DSN)

        try:
            Consumer(conn).run()
        except KeyboardInterrupt:
            logger.info("Shutting down.")
