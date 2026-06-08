import jwt
from datetime import datetime, timedelta, UTC

from django.conf import settings
from django.shortcuts import get_object_or_404

from auth_app.models import RefreshToken, User


class AuthService:
    @staticmethod
    def login(email: str, password: str) -> dict:
        user = get_object_or_404(User, email=email)

        if not user or not user.is_active or not user.check_password(password):
            raise ValueError("Invalid credentials")

        tokens = AuthService._generate_tokens(user)
        AuthService._save_refresh_token(user, tokens["refresh_token"])

        return tokens
    
    @staticmethod
    def logout(user):
        if isinstance(user, User):
            token = RefreshToken.objects.filter(user=user)
            if token:
                token.delete()
    
    @staticmethod
    def delete(user):
        user.is_active = False
        user.save()
        AuthService.logout(user)
    
    @staticmethod
    def is_exist_refresh_token(user):
        return RefreshToken.objects.filter(user=user)

    @staticmethod
    def validate_token(token):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.SIGN_TOKEN_ALGORITHM]
            )

            user = User.objects.get(id=payload.get('user_id'))

            if not user.is_active:
                raise ValueError("Invalid credentials")

            return user
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    @staticmethod
    def _generate_tokens(user) -> dict:
        access_payload = {
            "user_id": user.id,
            "exp": datetime.now(UTC) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXP_MINUTES),
            "type": "access",
        }
        refresh_payload = {
            "user_id": user.id,
            "exp": datetime.now(UTC) + timedelta(
                minutes=settings.REFRESH_TOKEN_EXP_MINUTES),
            "type": "refresh",
        }

        access_token = jwt.encode(
            access_payload,
            settings.SECRET_KEY,
            algorithm=settings.SIGN_TOKEN_ALGORITHM
        )
        refresh_token = jwt.encode(
            refresh_payload,
            settings.SECRET_KEY,
            algorithm=settings.SIGN_TOKEN_ALGORITHM
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @staticmethod
    def _save_refresh_token(user, token: str) -> None:
        RefreshToken.objects.create(user=user, token=token)
