from rest_framework.response import Response
from rest_framework.views import APIView
from ubiquity_users.serializers import UserSerializer


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

