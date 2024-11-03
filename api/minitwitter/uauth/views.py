from django.http.request import QueryDict
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.views import InvalidToken, TokenError

from .serializers import APITokenObtainPairSerializer, APITokenRefreshSerializer


class AuthViewSet(ViewSet):
    @extend_schema(
        request=APITokenObtainPairSerializer,
        responses={201: APITokenRefreshSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[],
        authentication_classes=[],
    )
    def login(self, request: Request) -> Response:
        return self._get_token(
            APITokenObtainPairSerializer,
            request.data,
        )

    @extend_schema(
        request=APITokenRefreshSerializer,
        responses={201: APITokenRefreshSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[],
        authentication_classes=[],
    )
    def refresh(self, request: Request) -> Response:
        return self._get_token(
            APITokenRefreshSerializer,
            request.data,
        )

    def _get_token(
        self,
        serializer: Serializer,
        data: QueryDict,
    ) -> Response:
        serializer = serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as err:
            raise InvalidToken(err.args[0])
        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )
