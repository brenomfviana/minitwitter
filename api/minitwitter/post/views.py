from uuid import uuid4

from common.pagination import FeedPagination
from common.serializers import create_paginated_serializer
from django.core.cache import cache
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from user.models import Follower

from .models import Like, Post
from .serializers import CreatePostSerializer, PostSerializer


class PostViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CreatePostSerializer,
        responses={201: PostSerializer},
    )
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

    @extend_schema(
        request=CreatePostSerializer,
        responses={201: PostSerializer},
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
        methods=["post"],
    )
    def reply(
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
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = Post.objects.create(
            user=request.user,
            is_reply=True,
            parent=post,
            **serializer.validated_data,
        )
        serializer = PostSerializer(instance=post)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

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


class FeedAPIView(APIView):
    pagination_class = FeedPagination
    permission_classes = [IsAuthenticated]

    cache_timeout = 60

    def _paginate_and_serialize(
        self,
        paginator: FeedPagination,
        queryset: QuerySet,
        request: Request,
    ) -> dict:
        paginated_feed = paginator.paginate_queryset(
            queryset=queryset,
            request=request,
        )
        serializer = PostSerializer(
            instance=paginated_feed,
            many=True,
        )
        return serializer.data

    @extend_schema(
        responses={201: create_paginated_serializer(PostSerializer)},
    )
    def get(self, request: Request) -> Response:
        paginator = self.pagination_class()

        page = request.query_params.get("page", 1)
        cache_key = f"user_feed_{request.user.id}_page_{page}"

        feed_data = cache.get(cache_key)

        if feed_data is None:
            following = Follower.objects.filter(
                follower=request.user,
            ).values_list(
                "following",
                flat=True,
            )
            feed = Post.objects.filter(
                user__in=following,
            ).order_by(
                "-created_at",
            )

            feed_data = self._paginate_and_serialize(
                queryset=feed,
                request=request,
                paginator=paginator,
            )

            cache.set(
                key=cache_key,
                value=feed_data,
                timeout=self.cache_timeout,
            )
        else:
            feed_data = self._paginate_and_serialize(
                queryset=feed_data,
                request=request,
                paginator=paginator,
            )

        return paginator.get_paginated_response(data=feed_data)
