from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from atlas.settings import logger
from enrol.models import EnrolRequest
from enrol.serializers import EnrolRequestSerializer, EnrolResponseSerializer
from member.authentication import ServiceAuthentication


REQUEST = 'REQUEST'


class EnrolRequestView(APIView):
    """
    Saves Enrol and registration requests and responses.
    """
    authentication_classes = (ServiceAuthentication, )

    @staticmethod
    def post(request):
        audit_log = request.data['audit_logs']

        for log in audit_log:
            log_type = log.get('audit_log_type')
            bink_message_uid = log.get('bink_message_uid')
            log['timestamp'] = datetime.fromtimestamp(log['timestamp'])

            # Flatten out for serializer
            log_data = {**log, **log.pop('payload')}

            if log_type == REQUEST:
                serializer = EnrolRequestSerializer(data=log_data)
            else:
                try:
                    request = EnrolRequest.objects.get(bink_message_uid=log['bink_message_uid'])
                except EnrolRequest.DoesNotExist as e:
                    logger.error(f'Request with bink_message_uid: {bink_message_uid} not found')
                    raise e

                log_data['request'] = request.id
                serializer = EnrolResponseSerializer(data=log_data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

        return Response('Data saved.', status=status.HTTP_201_CREATED)
