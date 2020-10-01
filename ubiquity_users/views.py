from datetime import datetime, timedelta

from azure.core.exceptions import ResourceExistsError
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.utils import OperationalError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from atlas.csv_writer import write_to_csv
from atlas.decorators import token_check
from atlas.settings import DELETED_UBIQUITY_USERS_CONTAINER, logger
from atlas.storage import create_blob_from_csv
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
            return Response(data='User saved: {}'.format(user_serializer.data), status=status.HTTP_201_CREATED)
        logger.warning('Method: UserSaveView: User Not saved {}'.format(request.data))
        return Response(data='User NOT saved: {}'.format(user_serializer.data), status=status.HTTP_400_BAD_REQUEST)


class UserBlobView(APIView):

    @staticmethod
    @token_check
    def get(request):
        time_24_hours_ago = datetime.now() - timedelta(days=1)
        list_for_csv = list()
        users = User.objects.filter(time_added_to_database__gte=time_24_hours_ago, delete=False)

        for user in users:
            list_for_csv.append({
                'email': user.email,
                'ubiquity_join_date': user.ubiquity_join_date,
                'opt_out_timestamp': user.time_added_to_database
            })

        try:
            deleted_users_csv = write_to_csv(list_for_csv)
        except IndexError as e:
            return Response(
                data='Method: UserBlobView.write_to_csv: {}'.format(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            create_blob_from_csv(deleted_users_csv, file_name='consents', base_directory='barclays',
                                 container=DELETED_UBIQUITY_USERS_CONTAINER)
        except (ResourceExistsError, ValueError) as e:
            logger.exception(
                'UserBlobView: Error saving to Blob storage - {} data - {}'.format(e, users))
            return Response(
                data='Error saving to blob storage - {} data - {}'.format(e, users),
                status=status.HTTP_400_BAD_REQUEST)

        for user in users:
            user.delete = True
            user.save()

        return Response(data=list_for_csv)


class HealthCheck(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response()


class ReadyzCheck(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        # Check DB
        db_conn = connections[DEFAULT_DB_ALIAS]
        try:
            db_conn.cursor()
        except OperationalError as err:
            return JsonResponse({"error": f"Cannot connect to database: {err}"}, status=500)

        return Response(status=204)
