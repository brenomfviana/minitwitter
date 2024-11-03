from rest_framework import serializers

from .models import Post


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "text",
            "image",
        ]
        extra_kwargs = {
            "text": {"write_only": True},
            "image": {"write_only": True},
        }


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["text"]
        extra_kwargs = {
            "text": {"write_only": True},
        }


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "text",
            "image",
            "user_username",
            "user_name",
            "like_count",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "text": {"read_only": True},
            "image": {"read_only": True},
            "user_username": {"read_only": True},
            "user_name": {"read_only": True},
            "like_count": {"read_only": True},
        }
