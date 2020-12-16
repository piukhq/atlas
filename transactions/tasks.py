from django.conf import settings

from transactions.merchant import get_merchant
from transactions.serializers import TransactionRequestSerializer
from atlas.settings import logger


def process_transaction(message: dict):
    try:
        merchant = get_merchant(message)
        merchant.process_message()

        serializer = TransactionRequestSerializer(data=merchant.audit_list, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except Exception as ex:
        logger.warning(f"process_transactions raised error: {repr(ex)}")
