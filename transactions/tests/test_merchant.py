import pytest

from transactions.merchant import HarveyNichols, Iceland, WasabiClub, get_merchant


# ====== Fixtures ======
@pytest.fixture
def harvey_nichols_message():
    return {
        "scheme_provider": "harvey-nichols",
        "response": {"outcome": "success"},
        "request": {
            "CustomerClaimTransactionRequest": {
                "token": "token",
                "customerNumber": "loyalty-hn-123",
                "id": "d482f186-df55-4da4-bc60-41890bf7a57d"
            }
        },
        "status_code": 200,
        "request_timestamp": "2020-09-02 13:44:14",
        "response_timestamp": "2020-09-02 13:44:14",
        "transactions": [
            {
                "transaction_id": "d482f186-df55-4da4-bc60-41890bf7a57d",
                "user_id": 0,
                "spend_amount": 1099,
                "transaction_date": "2020-05-28 15:46:00"
            }
        ]
    }


@pytest.fixture
def iceland_message():
    return {
        "scheme_provider": "iceland-bonus-card",
        "response": "",
        "request": {
            "json": {
                "message_uid": "39dd9217-af99-443a-ab52-fcc248af8d29",
                "transactions": [
                    {
                        "record_uid": "v8vzj4ykl7g28d6mln9x05m31qpeor27",
                        "merchant_scheme_id1": "v8vzj4ykl7g28d6mln9x05m31qpeor27",
                        "merchant_scheme_id2": "test-mid-123",
                        "transaction_id": "75aff1fa-17e9-40e1-bbc9-92f7daffca38"
                    },
                    {
                        "record_uid": "v8vzj4ykl7g28d6mln9x05m31qpeor27",
                        "merchant_scheme_id1": "v8vzj4ykl7g28d6mln9x05m31qpeor27",
                        "merchant_scheme_id2": "test-mid-123",
                        "transaction_id": "11a87408-d4d3-451b-b916-11a4b7c964a1"
                    }
                ]
            }
        },
        "status_code": 200,
        "request_timestamp": "2020-08-27 15:23:13",
        "response_timestamp": "2020-09-02 13:44:14",
        "transactions": [
            {
                "transaction_id": "75aff1fa-17e9-40e1-bbc9-92f7daffca38",
                "user_id": 0,
                "spend_amount": 1099,
                "transaction_date": "2020-06-02 15:46:00"
            },
            {
                "transaction_id": "11a87408-d4d3-451b-b916-11a4b7c964a1",
                "user_id": 0,
                "spend_amount": 1222,
                "transaction_date": "2020-06-02 15:47:45"
            }
        ]
    }


@pytest.fixture
def wasabi_message():
    return {
        "scheme_provider": "wasabi-club",
        "response": "",
        "request": {
            "origin_id": "6A0A65106BAA57B864E70CDCC28337E15EDED8EB",
            "ReceiptNo": "d482f186-df55-4da4-bc60-41890bf7a57d"
        },
        "status_code": 200,
        "request_timestamp": "2020-09-02 13:44:14",
        "response_timestamp": "2020-09-02 13:44:14",
        "transactions": [
            {
                "transaction_id": "d482f186-df55-4da4-bc60-41890bf7a57d",
                "user_id": 0,
                "spend_amount": 1099,
                "transaction_date": "2020-05-28 15:46:00"
            }
        ]
    }


# ====== Tests ======
def test_get_harvey_nichols(harvey_nichols_message):
    merchant = get_merchant(message=harvey_nichols_message)
    merchant.process_message()
    assert isinstance(merchant, HarveyNichols)


def test_get_iceland(iceland_message):
    merchant = get_merchant(message=iceland_message)
    merchant.process_message()
    assert isinstance(merchant, Iceland)


def test_get_wasabi(wasabi_message):
    merchant = get_merchant(message=wasabi_message)
    merchant.process_message()
    assert isinstance(merchant, WasabiClub)
