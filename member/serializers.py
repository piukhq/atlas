from datetime import datetime

from rest_framework import serializers

from .models import Member, Request, Response
from atlas.settings import logger


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'


REQUEST = 'REQUEST'


def save_request_audit(request_response):
    for log in request_response:
        log_type = log.get('audit_log_type')
        bink_message_uid = log.get('bink_message_uid')

        # Convert to datetime object
        log['timestamp'] = datetime.fromtimestamp(log['timestamp'])

        if log_type == REQUEST:
            # Check if member exists, if not create one to associate the request to.
            try:
                member = Member.objects.get(email=log['payload']['email'])
            except Member.DoesNotExist:
                member_serializer = MemberSerializer(data=log['payload'])
                if member_serializer.is_valid(raise_exception=True):
                    member = member_serializer.save()

            log['member'] = member.id
            serializer = RequestSerializer(data=log)

        else:
            # Get corresponding request object to associate response to.
            try:
                request = Request.objects.get(bink_message_uid=log['bink_message_uid'])
            except Request.DoesNotExist as e:
                logger.error(f'Request with bink_message_uid: {bink_message_uid} not found')
                raise e

            log['request'] = request.id
            serializer = ResponseSerializer(data=log)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
