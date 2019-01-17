from rest_framework.response import Response
from rest_framework.views import APIView
from ubiquity_users.serializers import UserSerializer
from datetime import datetime, timedelta
from ubiquity_users.models import User
from atlas.storage import create_blob_from_json
from azure.common import AzureException
from django.http import HttpResponse
from django.core import serializers


class UserSaveView(APIView):
    """
    View that saves user data to database
    """
    @staticmethod
    def post(request):
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data='User saved: {}'.format(user_serializer.data), status=201)
        return Response(data='User NOT saved: {}'.format(user_serializer.data), status=400)


class UserBlobView(APIView):

    @staticmethod
    def get(request):

        time_24_hours_ago = datetime.now() - timedelta(days=1)
        users = User.objects.filter(time_added_to_database__gte=time_24_hours_ago, delete=False)
        users_json = serializers.serialize('json', users)

        try:
            create_blob_from_json(users, file_name='consent', base_directory='directory',
                                  container='scheme')
        except AzureException as e:
            # logger.exception(
            #     'TransactionBlobView: Error saving to Blob storage - {} data - {}'.format(e, trans))
            return Response(
                data='Error saving to blob storage - {}'.format(e),
                status=e.status_code)

        for user in users:
            user.delete = True
            user.save()

        return HttpResponse(users_json, content_type='application/json')
