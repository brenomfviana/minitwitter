from django.contrib.auth.hashers import make_password
from user.models import Follower, User

from .factories import UserFactory


def user_stub(**kwargs):
    stub = UserFactory.build(**kwargs)
    return stub


def given_a_user(
    followers: list[User] = None,
    **kwargs,
):
    if followers is None:
        followers = []
    if "password" in kwargs:
        kwargs["password"] = make_password("password")
    user = UserFactory.create(**kwargs)
    for follower in followers:
        when_follow(
            follower=follower,
            following=user,
        )
    return user


def when_follow(
    follower: User,
    following: User,
):
    Follower.objects.create(
        follower=follower,
        following=following,
    )
