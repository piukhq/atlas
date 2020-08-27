from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MembershipRequest
from atlas.settings import logger
from membership.serializers import MembershipRequestSerializer
from membership.authentication import ServiceAuthentication


REQUEST = 'REQUEST'


class MembershipRequestView(APIView):
    """
    Saves Membership and registration requests and responses.
    """
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

                serializer = MembershipRequestSerializer(data=log_data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            else:
                message_uid = log['message_uid']
                try:
                    membership_request = MembershipRequest.objects.get(message_uid=message_uid)
                except MembershipRequest.DoesNotExist as e:
                    logger.error(f'No request with the message_uid - {message_uid}')
                    raise e

                membership_request.status_code = log['status_code']
                membership_request.response_body = log['response_body']
                membership_request.response_timestamp = datetime.fromtimestamp(log['timestamp'])
                membership_request.save()

        return Response('Data saved.', status=status.HTTP_201_CREATED)
