from django.contrib.auth.hashers import make_password
from factory import LazyAttribute, Sequence
from factory.django import DjangoModelFactory
from factory.faker import Faker as FactoryFaker
from faker import Faker
from user.models import User

from common.models import BaseModel


class BaseModelFactory(DjangoModelFactory):
    class Meta:
        model = BaseModel
        abstract = True

    id = FactoryFaker(provider="uuid4", cast_to=None)


DEFAULT_PASSWORD = "11111111"


class UserFactory(BaseModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f"{Faker().user_name()}{n}")
    email = LazyAttribute(lambda x: f"{x.username}@example.net")
    password = make_password(DEFAULT_PASSWORD)
    is_staff = False
    is_superuser = False
