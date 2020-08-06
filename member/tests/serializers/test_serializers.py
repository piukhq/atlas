from datetime import datetime

import pytest

from member.serializers import EnrolSerializer
from member.tests.factories import EnrolFactory


@pytest.fixture
def enrol_data():
    return EnrolFactory()


@pytest.mark.django_db
def test_enrol_factory(enrol_data):
    serializer = EnrolSerializer(enrol_data)
    data = serializer.data

    assert data['email'] == enrol_data.email
    assert data['title'] == enrol_data.title
    assert data['first_name'] == enrol_data.first_name
    assert data['last_name'] == enrol_data.last_name
    assert data['phone_number'] == enrol_data.phone_number
    assert data['membership_plan'] == enrol_data.membership_plan
    assert data['channel'] == enrol_data.channel
    assert data['http_response_code'] == enrol_data.http_response_code
    assert data['response_body'] == enrol_data.response_body
    assert data['payload'] == enrol_data.payload
    assert data['request_datetime'] == datetime.strftime(enrol_data.request_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
    assert data['response_datetime'] == datetime.strftime(enrol_data.response_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
