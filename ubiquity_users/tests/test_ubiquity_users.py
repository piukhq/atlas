import datetime
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from atlas.settings import ATLAS_SERVICE_AUTH_HEADER
from ubiquity_users.models import User


class TestUserSave(APITestCase):

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
        self.invalid_date = {
            'email': 'ct@test.com',
            'opt_out_timestamp': '21-01-2019 09:22:57'
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

    def test_invalid_date(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.post(self.url, self.invalid_date, format='json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_no_authorization_provided(self):
        resp = self.client.post(self.url, self.invalid_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 0)


class TestUbiquityBlobView(APITestCase):

    def setUp(self):
        self.auth_headers = ATLAS_SERVICE_AUTH_HEADER
        self.url = reverse('storage')
        self.user_data = User.objects.create(
            time_added_to_database=datetime.datetime.now(),
            email='ctoal@test.com',
            opt_out_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            delete='False'
        )
        self.user_data.refresh_from_db()

    @patch('ubiquity_users.views.write_to_csv')
    @patch('ubiquity_users.views.create_blob_from_csv')
    def test_nested_methods_were_called(self, mock_create_blob, mock_write_to_csv):
        mock_write_to_csv.return_value = 'email,opt_out_timestamp,ct@bink.com,{}'.format(
            self.user_data.opt_out_timestamp)

        self.user_data.save()

        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        self.client.get(self.url)

        self.assertEqual(len(mock_write_to_csv.call_args[0]), 1)
        self.assertEqual(len(mock_create_blob.call_args), 2)
        self.assertEqual(len(mock_create_blob.call_args[0]), 1)
        self.assertEqual(len(mock_create_blob.call_args[1]), 3)

    @patch('ubiquity_users.views.write_to_csv')
    @patch('ubiquity_users.views.create_blob_from_csv')
    def test_delete_is_set_to_true_after_save_to_blob(self, mock_create_blob, mock_write_to_csv):
        mock_write_to_csv.return_value = 'email,opt_out_timestamp,ct@bink.com,{}'.format(
            self.user_data.opt_out_timestamp)

        self.user_data.save()
        user_object_before_call = User.objects.get(email='ctoal@test.com')

        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.get(self.url)

        user_object_after_call = User.objects.get(email='ctoal@test.com')
        mock_create_blob.assert_called_with(
            'email,opt_out_timestamp,ct@bink.com,{}'.format(user_object_before_call.opt_out_timestamp),
            file_name='consents',
            base_directory='barclays',
            container='deleted-users-test')

        self.assertFalse(user_object_before_call.delete)
        self.assertTrue(user_object_after_call.delete)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @patch('ubiquity_users.views.write_to_csv')
    @patch('ubiquity_users.views.create_blob_from_csv')
    def test_response_returns_json(self, mock_create_blob, mock_write_to_csv):
        mock_write_to_csv.return_value = 'email,opt_out_timestamp,ct@bink.com,{}'.format(
            self.user_data.opt_out_timestamp)

        self.user_data.save()

        self.client.credentials(HTTP_AUTHORIZATION=self.auth_headers)
        resp = self.client.get(self.url)

        self.assertTrue(type(resp.data) is str)
        self.assertEqual(resp.content_type, 'application/json')
