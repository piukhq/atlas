import logging

from django.core.management.base import BaseCommand
from django.conf import settings
import kombu
import kombu.mixins

from transactions import tasks


log = logging.getLogger(__name__)


class Consumer(kombu.mixins.ConsumerMixin):
    def __init__(self, connection):
        self.queues = [kombu.Queue(settings.TRANSACTION_QUEUE)]
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(self.queues, callbacks=[self.on_message])]

    def on_message(self, body, message):
        log.info(f"Received transaction message.")
        tasks.process_transaction(body)
        message.ack()


class Command(BaseCommand):
    help = "Consume auth transactions from the specified queue"

    def handle(self, *args, **options):
        self.stdout.write(f"Consuming from queue: {settings.TRANSACTION_QUEUE}")
        conn = kombu.Connection(settings.AMQP_DSN)

        try:
            Consumer(conn).run()
        except KeyboardInterrupt:
            self.stdout.write("Shutting down.")
