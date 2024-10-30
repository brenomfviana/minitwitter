from rest_framework import serializers

from .models import Post


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["text"]
        extra_kwargs = {
            "text": {"write_only": True},
        }


class PostSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(
        source="user.username",
        read_only=True,
    )
    user_name = serializers.CharField(
        source="user.name",
        read_only=True,
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "text",
            "user_username",
            "user_name",
            "like_count",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "text": {"read_only": True},
            "user_username": {"read_only": True},
            "user_name": {"read_only": True},
            "like_count": {"read_only": True},
        }
