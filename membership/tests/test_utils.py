from django.test import TestCase

from membership.views import MembershipRequestView


class TestUtils(TestCase):

    def test_flatten_dict(self):
        payload = {"CustomerSignUp": {"email": "test@e.mail", "first_name": "Bonk"}}
        expected = {"email": "test@e.mail", "first_name": "Bonk"}

        flattened_dict = MembershipRequestView().flatten_dict(payload)

        self.assertEqual(flattened_dict, expected)

    def test_map_credentials(self):
        hn = {"email": "test@e.mail", "forename": "Bonky", "surname": "Bonk"}
        ice = {"email": "test@e.mail", "town_city": "Hastings", "phone1": "0800 00 1066"}

        expected_hn = {"email": "test@e.mail", "first_name": "Bonky", "last_name": "Bonk"}
        expected_ice = {"email": "test@e.mail", "city": "Hastings", "phone_number": "0800 00 1066"}

        actual_hn = MembershipRequestView().map_credentials(credentials=hn, slug="harvey-nichols")
        actual_ice = MembershipRequestView().map_credentials(credentials=ice, slug="iceland-bonus-card")

        self.assertEqual(expected_hn, actual_hn)
        self.assertEqual(expected_ice, actual_ice)

    def test_email_callback_url(self):
        ice = {"email": "", "callback_url": None}

        expected_ice = {"email": "", "callback_url": None}

        actual_ice = MembershipRequestView().map_credentials(credentials=ice, slug="iceland-bonus-card")

        self.assertEqual(expected_ice, actual_ice)
