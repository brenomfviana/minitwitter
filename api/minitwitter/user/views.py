from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import User
from .serializers import UserSerializer


class UserViewSet(ViewSet):
    def create(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
