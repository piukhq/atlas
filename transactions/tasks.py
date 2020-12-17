import sentry_sdk

from transactions.merchant import get_merchant
from transactions.serializers import TransactionRequestSerializer


def process_transaction(message: dict):
    try:
        merchant = get_merchant(message)
        merchant.process_message()

        serializer = TransactionRequestSerializer(data=merchant.audit_list, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except Exception:
        # we capture manually as we don't want these failures to crash the process
        sentry_sdk.capture_exception()
