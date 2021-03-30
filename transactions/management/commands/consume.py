import logging

import sentry_sdk

from django.core.management.base import BaseCommand
from django.conf import settings
import kombu
import kombu.mixins

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
            message.ack()
        except Exception as ex:
            # we capture manually as we don't want these failures to crash the process
            event_id = sentry_sdk.capture_exception()
            logger.warning(
                f"tasks.process_transaction raised exception: {repr(ex)}. "
                f"Sentry event ID: {event_id}"
            )


class Command(BaseCommand):
    help = "Consume auth transactions from the specified queue"

    def handle(self, *args, **options):
        logger.info(f"Consuming from queue: {settings.TRANSACTION_QUEUE}")
        conn = kombu.Connection(settings.AMQP_DSN)

        try:
            Consumer(conn).run()
        except KeyboardInterrupt:
            logger.info("Shutting down.")