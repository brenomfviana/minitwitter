from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken


class APITokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "Incorrect username or password!",
    }

    def get_token(self, user):
        token = RefreshToken().for_user(user)
        return token


class APITokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        return super().validate(attrs)
