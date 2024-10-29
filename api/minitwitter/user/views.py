from uuid import uuid4

from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Follower, User
from .serializers import CreateUserSerializer, UserProfileSerializer


class UserViewSet(ViewSet):
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def create(self, request: Request) -> Response:
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["password"] = make_password(data["password"])
        user = User.objects.create(**data)
        serializer = UserProfileSerializer(instance=user)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["patch"],
    )
    def follow(
        self,
        request: Request,
        pk: uuid4,
    ) -> Response:
        try:
            to_follow = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        Follower.objects.create(
            following=to_follow,
            follower=request.user,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["patch"],
    )
    def unfollow(
        self,
        request: Request,
        pk: uuid4,
    ) -> Response:
        try:
            follower = Follower.objects.get(
                following__id=pk,
                follower=request.user,
            )
            follower.delete()
        except Follower.DoesNotExist:
            return Response(
                {"error": "User not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get"],
    )
    def profile(
        self,
        request: Request,
        pk: uuid4,
    ) -> Response:
        try:
            user = User.objects.get(pk=pk)
            serializer = UserProfileSerializer(instance=user)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
