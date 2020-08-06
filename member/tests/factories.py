from datetime import datetime

import factory
import factory.fuzzy
from faker import Factory

from member.models import Enrol


CHANNELS = [
    'bink',
    'barclays',
    'fat_face'
]

faker = Factory.create(locale='en_GB')


class EnrolFactory(factory.DjangoModelFactory):
    class Meta:
        model = Enrol

    email = faker.email()
    title = faker.prefix()
    first_name = faker.first_name()
    last_name = faker.last_name()
    phone_number = faker.phone_number()
    request_datetime = datetime.now()
    membership_plan = 'test_membership_plan'
    channel = factory.fuzzy.FuzzyChoice(CHANNELS)
    http_response_code = 201
    response_body = {
        "email": faker.email(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name()
    }
    payload = {
        "email": faker.email(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name()
    }
    response_datetime = datetime.now()
