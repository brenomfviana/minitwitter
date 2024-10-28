from django.test import TestCase as DjangoTestCase
from rest_framework.test import APITestCase as DRFAPITestCase
from user.models import User

from common.test_utils.factories import DEFAULT_PASSWORD


class BaseTestCase(DjangoTestCase):
    pass


class APITestCase(DRFAPITestCase, BaseTestCase):
    def setUp(self):
        super().setUp()

        self.api = self.client
        self.client = None
        self.last_login = None

    def login(
        self,
        user: User,
        password=DEFAULT_PASSWORD,
    ):
        response = self.api.post(
            path="/api/auth/login/",
            data={
                "username": user.username,
                "password": password,
            },
            format="json",
        )
        self.last_login = response.data
        return self._credentials()

    def _credentials(self):
        access_token: str = self.last_login["access"]
        return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
