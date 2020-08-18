from datetime import datetime

import pytest

from enrol.serializers import EnrolRequestSerializer, EnrolResponseSerializer
from enrol.tests.factories import EnrolRequestFactory, EnrolResponseFactory


# ====== Fixtures ======
@pytest.fixture
def request_data():
    return EnrolRequestFactory()


@pytest.fixture
def response_data():
    return EnrolResponseFactory()


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
    assert data['timestamp'] == datetime.strftime(request_data.timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    assert data['integration_service'] == request_data.integration_service


@pytest.mark.django_db
def test_response_serializer(response_data):
    serializer = EnrolResponseSerializer(response_data)
    data = serializer.data

    assert data['status_code'] == response_data.status_code
