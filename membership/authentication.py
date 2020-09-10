from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from django.utils.translation import gettext_lazy as _

from django.conf import settings


class ServiceUser(AnonymousUser):
    def is_authenticated(self):
        return True

    uid = 'api_user'


class ServiceAuthentication(BaseAuthentication):
    """
    Authentication for olympus services
    """

    def get_token_type(self, request):
        auth = get_authorization_header(request).split()
        return self.check_token(auth), auth[0].lower()

    def get_token(self, request, token_name=b'token'):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != token_name:
            return None
        return self.check_token(auth)

    @staticmethod
    def check_token(auth):
        if len(auth) <= 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        return token

    def authenticate_credentials(self, key):
        if key != settings.SERVICE_API_KEY:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        return ServiceUser(), None

    def authenticate(self, request):
        return self.authenticate_credentials(self.get_token(request))
