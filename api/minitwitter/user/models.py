from common.models import BaseModel
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.functional import cached_property


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(
        verbose_name="username",
        max_length=20,
        unique=True,
        validators=[UnicodeUsernameValidator],
    )
    email = models.EmailField(
        verbose_name="email address",
        unique=True,
    )
    name = models.CharField(
        verbose_name="user name",
        max_length=200,
    )
    password = models.CharField(
        verbose_name="user password",
        max_length=150,
    )

    is_active = models.BooleanField(
        verbose_name="is active?",
        default=True,
    )
    is_staff = models.BooleanField(
        "is staff?",
        default=False,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"User ({self.username})"

    @cached_property
    def followers_count(self):
        return Follower.objects.filter(following=self).count()

    @cached_property
    def following_count(self):
        return Follower.objects.filter(follower=self).count()


class Follower(BaseModel):
    following = models.ForeignKey(
        verbose_name="following",
        to=User,
        on_delete=models.CASCADE,
        related_name="followings",
    )
    follower = models.ForeignKey(
        verbose_name="follower",
        to=User,
        on_delete=models.CASCADE,
        related_name="followers",
    )

    class Meta:
        unique_together = ("following", "follower")
        ordering = ["-created_at"]
        verbose_name = "Follower"
        verbose_name_plural = "Followers"

    def __str__(self):
        return f"User {self.follower.username} follows User {self.following.username}"
