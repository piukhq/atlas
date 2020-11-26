from json import loads


class BaseMerchant:
    def __init__(self, message: dict):
        self.scheme_name = message['scheme_provider']
        self.request = message.get('request')
        self.transactions = message['transactions']

        self.audit_data = {
            'status_code': message['status_code'],
            'request_timestamp': message['request_timestamp'],
            'response_timestamp': message['response_timestamp'],
            'request': self.request,
            'response': message['response'],
            'membership_plan': self.scheme_name
        }

        self.audit_list = []

    def process_message(self):
        pass


class HarveyNichols(BaseMerchant):
    def process_message(self):
        transaction_data = self.audit_data.copy()
        transaction_data['customer_number'] = self.request['CustomerClaimTransactionRequest']['customerNumber']
        transaction_data['transaction_id'] = self.transactions[0]['transaction_id']
        self.audit_list.append(transaction_data)


class Iceland(BaseMerchant):
    def process_message(self):
        request_body = loads(self.request['body'])

        for transaction in request_body['transactions']:
            transaction_data = self.audit_data.copy()
            transaction_data['message_uid'] = request_body['message_uid']
            transaction_data['transaction_id'] = transaction['transaction_id']
            transaction_data['record_uid'] = transaction['record_uid']
            transaction_data['customer_number'] = transaction['merchant_scheme_id2']
            self.audit_list.append(transaction_data)


class WasabiClub(BaseMerchant):
    def process_message(self):
        transaction_data = self.audit_data.copy()
        transaction_data['customer_number'] = self.request["origin_id"]
        transaction_data['transaction_id'] = self.transactions["ReceiptNo"]
        self.audit_list.append(transaction_data)


def get_merchant(message: dict):
    mapping = {
        'iceland-bonus-card': Iceland(message=message),
        'harvey-nichols': HarveyNichols(message=message),
        'wasabi-club': WasabiClub(message=message)
    }

    return mapping.get(message['scheme_provider'])
