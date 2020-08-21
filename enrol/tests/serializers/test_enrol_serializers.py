from datetime import datetime

import pytest

from enrol.serializers import EnrolRequestSerializer
from enrol.tests.factories import EnrolRequestFactory


# ====== Fixtures ======
@pytest.fixture
def request_data():
    return EnrolRequestFactory()


@pytest.fixture
def request_dict_data():
    return {
        "channel": "com.bink.wallet",
        "membership_plan_slug": "some-plan-slug",
        "handler_type": "JOIN",
        "bink_message_uid": "51bc9486-db0c-11ea-b8e5-acde48001122",
        "bink_record_uid": "pym1834v0zrqxnrz5e3wjdglepko5972",
        "request_timestamp": datetime.now(),
        "integration_service": "SYNC",
        "callback_url": "http://localhost:8000/join/merchant/iceland-bonus-card",
        "title": "Mr",
        "first_name": "Bonky",
        "last_name": "Bonk",
        "email": "kaziz2@binktest.com",
        "postcode": "SL56RE",
        "address_1": "8",
        "address_2": "Street",
        "town_city": "Rapture",
        "county": "County",
        "country": "GB",
        "dob": "2000-12-12",
        "phone1": "02084444444",
        "payload": {
            "title": "Mr",
            "first_name": "Bonky",
            "last_name": "Bonk",
            "email": "kaziz2@binktest.com",
            "postcode": "SL56RE",
            "address_1": "8",
            "address_2": "Street",
            "town_city": "Rapture",
            "county": "County",
            "country": "GB",
            "marketing_opt_in": True,
            "marketing_opt_in_thirdparty": False,
            "merchant_scheme_id1": "oydgerxzp4k97w0pql2n0q2lo183j5mv",
            "merchant_scheme_id2": None,
            "dob": "2000-12-12",
            "phone1": "02084444444"
        },
        "response_timestamp": datetime.now(),
        "status_code": 200,
        'response_body': 'OK'
    }


# ====== Tests =======
@pytest.mark.django_db
def test_request_serializer(request_data):
    serializer = EnrolRequestSerializer(request_data)
    data = serializer.data

    assert data['email'] == request_data.email
    assert data['title'] == request_data.title
    assert data['first_name'] == request_data.first_name
    assert data['request_timestamp'] == datetime.strftime(request_data.request_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    assert data['integration_service'] == request_data.integration_service
    assert data['status_code'] == request_data.status_code
    assert data['bink_message_uid'] == str(request_data.bink_message_uid)
    assert data['channel'] == request_data.channel
    assert data['payload'] == request_data.payload


@pytest.mark.django_db
def test_request_serializer_is_valid(request_dict_data):
    serializer = EnrolRequestSerializer(data=request_dict_data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()

    assert str(instance.bink_message_uid) == request_dict_data['bink_message_uid']
