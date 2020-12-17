import logging

import sentry_sdk

from transactions.merchant import get_merchant
from transactions.serializers import TransactionRequestSerializer

logger = logging.getLogger(__name__)


def process_transaction(message: dict):
    try:
        merchant = get_merchant(message)
        merchant.process_message()

        serializer = TransactionRequestSerializer(data=merchant.audit_list, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except Exception as ex:
        # we capture manually as we don't want these failures to crash the process
        event_id = sentry_sdk.capture_exception()
        logger.error(
            f"process_transaction raised exception: {repr(ex)}. "
            f"Sentry event ID: {event_id}"
        )
