import kombu

from django.conf import settings


class MessageQueue:
    def __init__(self, queue_name):
        self.queue_dsn = settings.RABBITMQ_DSN
        self.queue_name = queue_name

    def read_message(self):
        with kombu.Connection(self.queue_dsn) as conn:
            message_queue = conn.SimpleQueue(self.queue_name)

            # Check if there's messages on the queue
            name, msg_count, consumer_count = message_queue.queue.queue_declare()

            if msg_count > 0:
                message = message_queue.get(block=True, timeout=1)
                message.ack()
                message_queue.close()

                return message.payload
            else:
                return
