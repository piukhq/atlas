from datetime import datetime

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from atlas.settings import ATLAS_SERVICE_AUTH_HEADER
from django.urls import reverse


# ====== Fixtures ======


@pytest.fixture
def enrol_save_url():
    return reverse('enrol_save')


@pytest.fixture
def auth_client():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=ATLAS_SERVICE_AUTH_HEADER)
    return client


@pytest.fixture
def enrol_data():
    return {
        "email": 'test_email@test.com',
        "title": 'Mr',
        "first_name": 'Steve',
        "last_name": 'Rogers',
        "phone_number": '02089991111',
        "request_datetime": str(datetime.now()),
        "membership_plan": 'test_membership_123',
        "http_response_code": 201,
        "response_body": {"msg": "test message"},
        "payload": {"email": 'test_email@test.com', 'membership_plan': 'test_membership_123'},
        "response_datetime": str(datetime.now())
    }


# ====== Tests ======

# SUCCESSFUL
@pytest.mark.django_db
def test_enrol_save_view(client, enrol_data, enrol_save_url):
    response = client.post(
        path=enrol_save_url,
        data=enrol_data,
        HTTP_AUTHORIZATION=ATLAS_SERVICE_AUTH_HEADER
    )

    assert response.status_code == status.HTTP_201_CREATED


# BAD REQUEST
def test_bad_request(client, enrol_save_url):
    response = client.post(
        path=enrol_save_url,
        data={'first_name': 'test_name'},
        HTTP_AUTHORIZATION=ATLAS_SERVICE_AUTH_HEADER
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# ====== Auth Tests ======


def test_fail_without_token(client, enrol_data, enrol_save_url):
    response = client.post(path=enrol_save_url, json=enrol_data)

    assert response.status_code == 403
    assert response.json()['detail'] == 'Incorrect authentication credentials.'
