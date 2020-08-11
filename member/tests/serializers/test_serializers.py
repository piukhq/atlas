from datetime import datetime

import pytest

from member.serializers import MemberSerializer, RequestSerializer, ResponseSerializer
from member.tests.factories import MemberFactory, RequestFactory, ResponseFactory


# ====== Fixtures ======

@pytest.fixture
def member_data():
    return MemberFactory()


@pytest.fixture
def request_data():
    return RequestFactory()


@pytest.fixture
def response_data():
    return ResponseFactory()


# ====== Tests =======


@pytest.mark.django_db
def test_member_serializer(member_data):
    serializer = MemberSerializer(member_data)
    data = serializer.data

    assert data['email'] == member_data.email
    assert data['title'] == member_data.title
    assert data['first_name'] == member_data.first_name
    assert data['last_name'] == member_data.last_name
    assert data['phone_number'] == member_data.phone_number
    assert data['password'] == member_data.password


@pytest.mark.django_db
def test_request_serializer(request_data):
    serializer = RequestSerializer(request_data)
    data = serializer.data

    assert data['payload'] == request_data.payload
    assert data['timestamp'] == datetime.strftime(request_data.timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    assert data['integration_service'] == request_data.integration_service


@pytest.mark.django_db
def test_response_serializer(response_data):
    serializer = ResponseSerializer(response_data)
    data = serializer.data

    assert data['status_code'] == response_data.status_code
