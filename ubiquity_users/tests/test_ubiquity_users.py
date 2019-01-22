from rest_framework.test import APITestCase, APIClient
from atlas.settings import ATLAS_SERVICE_AUTH_HEADER
from ubiquity_users.models import User
from django.urls import reverse
from rest_framework import status


class TestBlobStorageEndpoint(APITestCase):

    def setUp(self):
        self.auth_headers = ATLAS_SERVICE_AUTH_HEADER
        self.url = reverse('ubiquity_postgres')
        self.data = {
            'email': 'ct@test.com',
            'opt_out_timestamp': '2019-01-21 09:22:57',
        }
        self.invalid_data = {
            'opt_out_timestamp': '2019-01-21 09:22:57',
        }
        self.client = APIClient()

    def test_good_payload_saves_to_database(self):

        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.post(self.url, self.data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'ct@test.com')

    def test_invalid_payload_returns_404(self):

        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.post(self.url, self.invalid_data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_no_authorization_provided(self):
        resp = self.client.post(self.url, self.invalid_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 0)
