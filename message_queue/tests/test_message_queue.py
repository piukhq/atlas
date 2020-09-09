import kombu
import pytest

from django.conf import settings
from message_queue.queue_agent import MessageQueue


# ====== Fixtures ======
@pytest.fixture
def rabbit_settings(settings):
    settings.CELERY_BROKER_URL = 'memory://'


# ====== Tests ======
def test_read_message(rabbit_settings):
    queue_name = 'test_queue'
    test_message = 'test message'

    # Add message to test queue
    with kombu.Connection(settings.CELERY_BROKER_URL) as conn:
        simple_queue = conn.SimpleQueue(queue_name)
        simple_queue.put(test_message)
        simple_queue.close()

    queue = MessageQueue('test_queue')
    message = queue.read_message()

    assert message == test_message
