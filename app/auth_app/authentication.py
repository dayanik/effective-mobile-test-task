from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from auth_app.services import AuthService
from django.contrib.auth.models import AnonymousUser


class CustomJWTAuthentication(BaseAuthentication):

    def _extract_token(self, request: Request):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            return auth_header.split()[1]

    def authenticate(self, request):
        token = self._extract_token(request)

        if not token:
            return None

        try:
            user = AuthService.validate_token(token)
            if not AuthService.is_exist_refresh_token(user):
                raise ValueError('User is logout')
        except ValueError:
            user = AnonymousUser

        return (user, token)
