from datetime import datetime

import pytest

from enrol.serializers import EnrolRequestSerializer
from enrol.tests.factories import EnrolRequestFactory


# ====== Fixtures ======
@pytest.fixture
def request_data():
    return EnrolRequestFactory()


# ====== Tests =======
@pytest.mark.django_db
def test_request_serializer(request_data):
    serializer = EnrolRequestSerializer(request_data)
    data = serializer.data

    assert data['email'] == request_data.email
    assert data['title'] == request_data.title
    assert data['first_name'] == request_data.first_name
    assert data['last_name'] == request_data.last_name
    assert data['phone_number'] == request_data.phone_number
    assert data['password'] == request_data.password
    assert data['card_number'] == request_data.card_number
    assert data['request_timestamp'] == datetime.strftime(request_data.request_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    assert data['integration_service'] == request_data.integration_service
    assert data['status_code'] == request_data.status_code
