import json
from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .mappings import SLUG_TO_CREDENTIAL_MAP
from .models import MembershipRequest
from atlas.settings import logger
from membership.serializers import MembershipRequestSerializer, MembershipResponseSerializer
from membership.authentication import ServiceAuthentication


REQUEST = 'REQUEST'


class MembershipRequestView(APIView):
    """
    Saves Membership and registration requests and responses.
    """
    authentication_classes = (ServiceAuthentication, )

    def post(self, request):
        audit_logs = request.data['audit_logs']

        for log in audit_logs:
            log_type = log.get('audit_log_type')

            if log_type == REQUEST:
                # Flatten out for serializer (name, address ect..)
                log_data = {
                    **log,
                    **self.flatten_dict(log['payload']),
                    'timestamp': datetime.fromtimestamp(log['timestamp'])
                }

                # Map credentials to model fields depending on scheme
                mapped_log_data = self.map_credentials(log_data, log['membership_plan_slug'])

                serializer = MembershipRequestSerializer(data=mapped_log_data)
            else:
                message_uid = log['message_uid']
                try:
                    membership_request = MembershipRequest.objects.only("id").get(message_uid=message_uid)
                except MembershipRequest.DoesNotExist as e:
                    logger.error(f'No request with the message_uid - {message_uid}')
                    raise e

                log_data = self.process_response(log, membership_request)
                serializer = MembershipResponseSerializer(data=log_data)

            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except ValidationError as e:
                logger.error(f"Error saving audit log - {e} - log data: {log_data}")
                raise

        return Response('Data saved.', status=status.HTTP_201_CREATED)

    def flatten_dict(self, obj: dict) -> dict:
        """
        Very niche method of flattening a dict due to the following:
            1 - If a value is a dict, the corresponding key is discarded.
            2 - Does not account for key name clashes and so conflicting names will be overwritten.
        """
        flattened_dict = {}
        for k, v in obj.items():
            if isinstance(v, dict):
                flattened_dict.update(self.flatten_dict(v))
            else:
                flattened_dict[k] = v
        return flattened_dict

    @staticmethod
    def map_credentials(credentials: dict, slug: str) -> dict:
        if slug not in SLUG_TO_CREDENTIAL_MAP:
            return credentials

        return {
            SLUG_TO_CREDENTIAL_MAP[slug].get(k, k): v
            for k, v in credentials.items()
        }

    def process_response(self, log: dict, membership_request: MembershipRequest) -> dict:
        log_data = {
            **log,
            'request': membership_request.id,
            'timestamp': datetime.fromtimestamp(log['timestamp']),
            'payload': log['payload'],
        }

        if isinstance(log['payload'], dict):
            flattened_log_data = {
                **log_data,
                **self.flatten_dict(log['payload']),
                'payload': json.dumps(log['payload']),
            }
            log_data = self.map_credentials(flattened_log_data, log['membership_plan_slug'])

        elif isinstance(log['payload'], str):
            try:
                flattened_log_data = {
                    **log_data,
                    **self.flatten_dict(json.loads(log['payload'])),
                    'payload': log['payload'],
                }
                log_data = self.map_credentials(flattened_log_data, log['membership_plan_slug'])

            except json.JSONDecodeError:
                return log_data

        # Update any fields that were not populated in the initial request e.g card_number
        req_serializer = MembershipRequestSerializer(membership_request, data=log_data)
        try:
            if req_serializer.is_valid(raise_exception=True):
                req_serializer.save()
        except ValidationError as e:
            logger.warning(
                f"Error occurred when updating MembershipRequest (id={membership_request.id}) \n"
                f"Data - {log_data} \n"
                f"ValidationError - {e}"
            )

        return log_data
