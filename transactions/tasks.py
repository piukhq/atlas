from transactions.serializers import AuditDataSerializer


def process_transaction(message: dict):
    audit_data_serializer = AuditDataSerializer(data=message)
    audit_data_serializer.is_valid(raise_exception=True)
    audit_data_serializer.save()
