from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from django.utils import timezone

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections


class WSTokenAuthMiddleware:
    """
    Token [Querystring/Header] authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        query_string = parse_qs(scope['query_string']) #Used for querystring token url auth
        headers = dict(scope['headers']) #Used for headers token url auth
        if b'token' in query_string:
            try:
                token_key = query_string[b'token'][0].decode()
                token = Token.objects.get(key=token_key)
                scope['user'] = token.user
                close_old_connections()
            except ApiToken.DoesNotExist:
                scope['user'] = AnonymousUser()
        elif b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Token':
                    token = Token.objects.get(key=token_key)
                    scope['user'] = token.user
                    close_old_connections()
            except ApiToken.DoesNotExist:
                scope['user'] = AnonymousUser()
        else:
            pass #Session auth or anonymus

        return self.inner(scope)


UniversalAuthMiddlewareStack = lambda inner: WSTokenAuthMiddleware(AuthMiddlewareStack(inner))
