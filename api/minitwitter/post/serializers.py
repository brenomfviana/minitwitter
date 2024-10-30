from rest_framework import serializers

from .models import Post


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["text"]


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
        ]
