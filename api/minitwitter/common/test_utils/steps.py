from django.contrib.auth.hashers import make_password
from post.models import Like, Post
from user.models import Follower, User

from .factories import PostFactory, UserFactory


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


def given_a_post(
    user=None,
    likers: list[User] = None,
    **kwargs,
):
    if user is None:
        user = given_a_user()
    if likers is None:
        likers = []
    kwargs.update({"user": user})
    post = PostFactory.create(**kwargs)
    for liker in likers:
        when_like(
            user=liker,
            post=post,
        )
    return post


def when_like(
    user: User,
    post: Post,
):
    Like.objects.create(
        user=user,
        post=post,
    )
