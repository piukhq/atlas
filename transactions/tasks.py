from transactions.merchant import get_merchant
from transactions.serializers import TransactionRequestSerializer


def process_transaction(message: dict):
    merchant = get_merchant(message)
    merchant.process_message()

    serializer = TransactionRequestSerializer(data=merchant.audit_list, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
