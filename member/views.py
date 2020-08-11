from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from atlas.decorators import token_check
from member.serializers import save_request_audit


class RequestResponseView(APIView):
    """
    View to save resquest and response
    """

    @staticmethod
    @token_check
    def post(request):
        audit_log = request.data['audit_log']
        save_request_audit(audit_log)

        return Response('Data saved.', status=status.HTTP_201_CREATED)
