from transactions.merchant import get_merchant
from transactions.serializers import AuditDataSerializer, TransactionRequestSerializer


def process_transaction(message: dict):
    # merchant = get_merchant(message)
    # merchant.process_message()

    # transaction_request_serializer = TransactionRequestSerializer(data=merchant.audit_list, many=True)
    # transaction_request_serializer.is_valid(raise_exception=True)
    # transaction_request_serializer.save()

    audit_data_serializer = AuditDataSerializer(data=message)
    audit_data_serializer.is_valid(raise_exception=True)
    audit_data_serializer.save()
