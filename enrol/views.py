from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from atlas.settings import logger
from enrol.models import EnrolRequest
from enrol.serializers import EnrolRequestSerializer
from enrol.authentication import ServiceAuthentication


REQUEST = 'REQUEST'


class EnrolRequestView(APIView):
    pass
#     """
#     Saves Enrol and registration requests and responses.
#     """
    authentication_classes = (ServiceAuthentication, )

    @staticmethod
    def post(request):
        audit_log = request.data['audit_logs']
        log_data = {}

        for log in audit_log:
            log_type = log.get('audit_log_type')

            if log_type == REQUEST:
                # Flatten out for serializer (name, address ect..)
                log_data = {**log, **log['payload']}
                log_data['request_timestamp'] = datetime.fromtimestamp(log['timestamp'])
            else:
                log_data = {**log_data, **log}
                log_data['response_timestamp'] = datetime.fromtimestamp(log['timestamp'])

        serializer = EnrolRequestSerializer(data=log_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response('Data saved.', status=status.HTTP_201_CREATED)
