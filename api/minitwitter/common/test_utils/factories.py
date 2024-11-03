from django.contrib.auth.hashers import make_password
from factory import LazyAttribute, LazyFunction, Sequence
from factory.django import DjangoModelFactory
from factory.faker import Faker as FactoryFaker
from faker import Faker
from post.models import Post
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

    username = Sequence(
        function=lambda n: f"{Faker().user_name()}{n}",
    )
    email = LazyAttribute(
        function=lambda x: f"{x.username}@email.com",
    )
    password = make_password(password=DEFAULT_PASSWORD)
    is_staff = False
    is_superuser = False


class PostFactory(BaseModelFactory):
    class Meta:
        model = Post

    text = LazyFunction(lambda: Faker().text(max_nb_chars=128))
