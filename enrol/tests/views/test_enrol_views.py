import pytest
from rest_framework import status

from django.urls import reverse

from atlas.settings import ATLAS_SERVICE_AUTH_HEADER
from enrol.models import EnrolRequest


# ====== Fixtures ======
@pytest.fixture
def enrol_url():
    return reverse('enrol_audit')


@pytest.fixture
def request_response_data():
    return {
        "audit_logs": [
            {
                "audit_log_type": "REQUEST",
                "channel": "com.bink.wallet",
                "membership_plan_slug": "some-plan-slug",
                "handler_type": "JOIN",
                "bink_message_uid": "51bc9486-db0c-11ea-b8e5-acde48001122",
                "bink_record_uid": "pym1834v0zrqxnrz5e3wjdglepko5972",
                "timestamp": 1597071345,
                "integration_service": "SYNC",
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
                    "record_uid": "pym1834v0zrqxnrz5e3wjdglepko5972",
                    "country": "GB",
                    "message_uid": "51bc9486-db0c-11ea-b8e5-acde48001122",
                    "callback_url": "http://localhost:8000/join/merchant/iceland-bonus-card",
                    "marketing_opt_in": True,
                    "marketing_opt_in_thirdparty": False,
                    "merchant_scheme_id1": "oydgerxzp4k97w0pql2n0q2lo183j5mv",
                    "merchant_scheme_id2": None,
                    "dob": "2000-12-12",
                    "phone1": "02084444444"
                }
            },
            {
                "audit_log_type": "RESPONSE",
                "channel": "com.bink.wallet",
                "membership_plan_slug": "some-plan-slug",
                "handler_type": "JOIN",
                "bink_message_uid": "51bc9486-db0c-11ea-b8e5-acde48001122",
                "bink_record_uid": "pym1834v0zrqxnrz5e3wjdglepko5972",
                "timestamp": 1597071345,
                "integration_service": "SYNC",
                "status_code": 200,
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
                    "record_uid": "pym1834v0zrqxnrz5e3wjdglepko5972",
                    "country": "GB",
                    "message_uid": "51bc9486-db0c-11ea-b8e5-acde48001122",
                    "callback_url": "http://localhost:8000/join/merchant/iceland-bonus-card",
                    "marketing_opt_in": True,
                    "marketing_opt_in_thirdparty": False,
                    "merchant_scheme_id1": "oydgerxzp4k97w0pql2n0q2lo183j5mv",
                    "merchant_scheme_id2": None,
                    "dob": "2000-12-12",
                    "phone1": "02084444444"
                },
                'response_body': 'OK'
            }
        ]
    }


# ====== Tests ======
@pytest.mark.django_db
def test_audit_log_save_view(client, request_response_data, enrol_url):
    response = client.post(
        path=enrol_url,
        data=request_response_data,
        HTTP_AUTHORIZATION=ATLAS_SERVICE_AUTH_HEADER,
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_201_CREATED

    request_data = request_response_data['audit_logs'][0]
    response_data = request_response_data['audit_logs'][1]

    enrol_request = EnrolRequest.objects.last()

    assert str(enrol_request.bink_message_uid) == request_data['bink_message_uid']
    assert enrol_request.status_code == response_data['status_code']


# ====== Auth Tests ======
def test_fail_without_token(client, request_response_data, enrol_url):
    response = client.post(path=enrol_url, json=request_response_data)

    assert response.status_code == 403
    assert response.json()['detail'] == 'Invalid token.'
