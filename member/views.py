from atlas.settings import logger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from atlas.decorators import token_check
from member.serializers import EnrolSerializer


class EnrolSaveView(APIView):
    """
    View to save enrol payload and response
    """

    @staticmethod
    @token_check
    def post(request):
        serializer = EnrolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data saved.', status=status.HTTP_201_CREATED)

        logger.warning(f'EnrolSaveView.post: Enrol data NOT saved {serializer.errors}.')
        return Response(
            data='Enrol data NOT saved: {}'.format(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
