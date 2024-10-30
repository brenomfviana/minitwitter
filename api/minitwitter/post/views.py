from uuid import uuid4

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Like, Post
from .serializers import CreatePostSerializer, PostSerializer


class PostViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = Post.objects.create(
            user=request.user,
            **serializer.validated_data,
        )
        serializer = PostSerializer(instance=post)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def update(
        self,
        request: Request,
        pk: uuid4,
    ) -> Response:
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query = Post.objects.filter(pk=pk)
        query.update(
            user=request.user,
            **serializer.validated_data,
        )
        post = query.last()
        serializer = PostSerializer(instance=post)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def delete(
        self,
        request: Request,
        pk: uuid4,
    ) -> Response:
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if request.user != post.user:
            return Response(
                {"error": "Post not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        post.delete()
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["patch"],
    )
    def like(
        self,
        request: Request,
        pk: uuid4,
    ) -> Response:
        try:
            to_like = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        Like.objects.create(
            post=to_like,
            user=request.user,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["patch"],
    )
    def unlike(
        self,
        request: Request,
        pk: uuid4,
    ) -> Response:
        try:
            like = Like.objects.get(
                post__pk=pk,
                user=request.user,
            )
            like.delete()
        except Like.DoesNotExist:
            return Response(
                {"error": "Post not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
