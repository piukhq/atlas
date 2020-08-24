from json import loads
from .serializers import TransactionRequestSerializer


def store_transaction_data(transaction_data):
    # TODO: Subscribe to queue to get data

    request_data = loads(transaction_data['request'])
    response_data = loads(transaction_data['response'])

    data = transaction_data.copy()

    data['customer_number'] = request_data.get('customer_number')
    data['membership_plan'] = request_data.get('membership_plan')
    data['request'] = request_data
    data['response'] = response_data

    serializer = TransactionRequestSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()

    return f'Transaction saved - {instance.transaction_id}'
