from datetime import datetime

import pytest
from django.utils import timezone

from membership.serializers import MembershipRequestSerializer, MembershipResponseSerializer
from membership.tests.factories import MembershipRequestFactory, MembershipResponseFactory


# ====== Fixtures ======
@pytest.fixture
def request_data():
    return MembershipRequestFactory()


@pytest.fixture
def request_dict_data():
    return {
        "channel": "com.bink.wallet",
        "membership_plan_slug": "some-plan-slug",
        "handler_type": "JOIN",
        "message_uid": "51bc9486-db0c-11ea-b8e5-acde48001122",
        "record_uid": "pym1834v0zrqxnrz5e3wjdglepko5972",
        "timestamp": timezone.now(),
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
            "phone1": "02084444444",
        },
    }


@pytest.fixture
def request_dict_data_null():
    return {
        "channel": "com.bink.wallet",
        "membership_plan_slug": "some-plan-slug",
        "handler_type": "VALIDATE",
        "message_uid": "51bc9486-db0c-11ea-b8e5-acde48001129",
        "record_uid": "pym1834v0zrqxnrz5e3wjdglepko5972",
        "timestamp": timezone.now(),
        "integration_service": "SYNC",
        "callback_url": None,
        "title": "Mr",
        "first_name": "Rahima",
        "last_name": "Tester",
        "email": "",
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
            "first_name": "Rahima",
            "last_name": "Tester",
            "email": "",
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
            "phone1": "02084444444",
        },
    }


@pytest.fixture
def response_data():
    return MembershipResponseFactory()


# ====== Tests =======
@pytest.mark.django_db
def test_request_serializer(request_data):
    serializer = MembershipRequestSerializer(request_data)
    data = serializer.data

    assert data["email"] == request_data.email
    assert data["title"] == request_data.title
    assert data["first_name"] == request_data.first_name
    assert data["date_of_birth"] == request_data.date_of_birth
    assert data["timestamp"] == datetime.strftime(request_data.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    assert data["integration_service"] == request_data.integration_service
    assert data["message_uid"] == str(request_data.message_uid)
    assert data["channel"] == request_data.channel
    assert data["payload"] == request_data.payload


@pytest.mark.django_db
def test_request_serializer_is_valid(request_dict_data):
    serializer = MembershipRequestSerializer(data=request_dict_data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()

    assert str(instance.message_uid) == request_dict_data["message_uid"]


@pytest.mark.django_db
def test_request_serializer_null_value(request_dict_data_null):
    serializer = MembershipRequestSerializer(data=request_dict_data_null)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()

    assert instance.email == request_dict_data_null["email"]
    assert instance.callback_url == request_dict_data_null["callback_url"]


@pytest.mark.django_db
def test_response_serializer(response_data):
    serializer = MembershipResponseSerializer(response_data)
    data = serializer.data

    assert data["status_code"] == response_data.status_code
    assert data["timestamp"] == datetime.strftime(response_data.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    assert data["response_body"] == str(response_data.response_body)
