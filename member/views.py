from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from member.authentication import ServiceAuthentication
from member.serializers import save_request_audit


class RequestResponseView(APIView):
    """
    View to save request and response
    """
    authentication_classes = (ServiceAuthentication, )

    @staticmethod
    def post(request):
        audit_logs = request.data
        save_request_audit(audit_logs)

        return Response('Data saved.', status=status.HTTP_201_CREATED)
