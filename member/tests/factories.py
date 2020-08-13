from datetime import datetime
from uuid import uuid4

import factory
import factory.fuzzy
from faker import Factory

from member.models import Member, Request, Response


CHANNELS = [
    'bink',
    'barclays',
    'fat_face'
]

INTEGRATION_SERVICE = [
    'async',
    'synchronous'
]

faker = Factory.create(locale='en_GB')


class MemberFactory(factory.DjangoModelFactory):
    class Meta:
        model = Member

    email = faker.email()
    title = faker.prefix()
    first_name = faker.first_name()
    last_name = faker.last_name()
    phone_number = faker.phone_number()
    password = faker.password()
    postcode = faker.postcode()
    address_1 = faker.street_address()
    city = faker.city()
    country = faker.country()
    card_number = '123456789'


class RequestFactory(factory.DjangoModelFactory):
    class Meta:
        model = Request

    member = factory.SubFactory(MemberFactory)
    payload = {
        'email': faker.email(),
        'first_name': faker.first_name(),
        "last_name": faker.last_name()
    }
    timestamp = datetime.now()
    integration_service = factory.fuzzy.FuzzyChoice(INTEGRATION_SERVICE)
    channel = factory.fuzzy.FuzzyChoice(CHANNELS)
    bink_message_uid = uuid4()
    bink_record_uid = 'testBinkRecordUID'
    membership_plan = 'test_membership_plan'
    callback_url = 'http://test-call-back-url'
    handler_type = 'JOIN'


class ResponseFactory(factory.DjangoModelFactory):
    class Meta:
        model = Response

    request = factory.SubFactory(RequestFactory)
    response_body = {
        "email": faker.email(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name()
    }
    timestamp = datetime.now()
    status_code = 200
