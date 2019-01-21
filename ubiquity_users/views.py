import json
from datetime import datetime, timedelta

from azure.common import AzureException
from django.core import serializers
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from atlas.decorators import token_check
from atlas.settings import logger
from atlas.storage import create_blob_from_csv
from atlas.csv_writer import write_to_csv
from ubiquity_users.models import User
from ubiquity_users.serializers import UserSerializer


class UserSaveView(APIView):
    """
    View that saves user data to database
    """
    @staticmethod
    @token_check
    def post(request):
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data='User saved: {}'.format(user_serializer.data), status=201)
        return Response(data='User NOT saved: {}'.format(user_serializer.data), status=400)


class UserBlobView(APIView):

    @staticmethod
    @token_check
    def get(request):

        time_24_hours_ago = datetime.now() - timedelta(days=1)

        users = User.objects.filter(time_added_to_database__gte=time_24_hours_ago, delete=False)
        users_json = serializers.serialize('json', users)
        user_dicts = json.loads(users_json)
        user_list_of_dicts = [d['fields'] for d in user_dicts]

        list_for_csv = [
            {k: v for k, v in d.items() if k == 'email' or k == 'opt_out_timestamp'} for d in user_list_of_dicts
        ]

        deleted_users_csv = write_to_csv(list_for_csv)

        try:
            create_blob_from_csv(deleted_users_csv, file_name='consents', base_directory='barclays',
                                 container='deleted-users-test')
        except AzureException as e:
            logger.exception(
                'UserBlobView: Error saving to Blob storage - {} data - {}'.format(e, users_json))
            return Response(
                data='Error saving to blob storage - {} data - {}'.format(e, users_json),
                status=e.status_code)

        for user in users:
            user.delete = True
            user.save()

        return HttpResponse(users_json, content_type='application/json')
