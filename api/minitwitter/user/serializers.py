from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "name",
            "password",
        ]
        extra_kwargs = {
            "email": {"write_only": True},
            "username": {"write_only": True},
            "name": {"write_only": True},
            "password": {"write_only": True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "name",
            "followers_count",
            "following_count",
            "posts_count",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"read_only": True},
            "username": {"read_only": True},
            "name": {"read_only": True},
            "followers_count": {"read_only": True},
            "following_count": {"read_only": True},
            "posts_count": {"read_only": True},
        }
