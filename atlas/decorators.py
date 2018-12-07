from atlas import settings


def token_check(fn):
    """
    Check if auth token is present
    """
    def _wrap(*args, **kwargs):
        request = args[1]
        using_service_token = False

        # Check if we are using the service token and therefore don't need to decrypt

        auth_token = request.META.get('HTTP_AUTHORIZATION')
        if auth_token and auth_token == settings.ATLAS_SERVICE_AUTH_HEADER:
            using_service_token = True

        return fn(using_service_token=using_service_token, *args, **kwargs)

    return _wrap
