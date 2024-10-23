from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

from common.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(verbose_name="username", max_length=20, unique=True, validators=[UnicodeUsernameValidator])
    email = models.EmailField(verbose_name="email address", unique=True)
    name = models.CharField(verbose_name="user name", max_length=200)
    password = models.CharField(verbose_name="user password", max_length=150)

    is_staff = models.BooleanField("is staff?", default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"User ({self.username})"
