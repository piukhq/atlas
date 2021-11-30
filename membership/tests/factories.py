from datetime import datetime
from uuid import uuid4

import factory.fuzzy
from faker import Factory

from membership.models import MembershipRequest, MembershipResponse

CHANNELS = ["bink", "barclays", "fat_face"]

INTEGRATION_SERVICE = ["async", "synchronous"]

faker = Factory.create(locale="en_GB")


class MembershipRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MembershipRequest

    email = faker.email()
    title = faker.prefix()
    first_name = faker.first_name()
    last_name = faker.last_name()
    date_of_birth = faker.date()
    phone_number = faker.phone_number()
    password = faker.password()
    postcode = faker.postcode()
    address_1 = faker.street_address()
    city = faker.city()
    country = faker.country()
    card_number = "123456789"
    timestamp = datetime.now()
    integration_service = factory.fuzzy.FuzzyChoice(INTEGRATION_SERVICE)
    channel = factory.fuzzy.FuzzyChoice(CHANNELS)
    message_uid = uuid4()
    record_uid = "testBinkRecordUID"
    membership_plan_slug = "test_membership_plan"
    callback_url = "http://test-call-back-url"
    handler_type = "JOIN"
    payload = {"payload": "test"}


class MembershipResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MembershipResponse

    request = factory.SubFactory(MembershipRequestFactory)
    response_body = {"email": faker.email(), "first_name": faker.first_name(), "last_name": faker.last_name()}
    timestamp = datetime.now()
    status_code = 200
