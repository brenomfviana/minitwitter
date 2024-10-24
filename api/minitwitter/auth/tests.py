from common.test_utils import APITestCase
from rest_framework import status
from user.models import User


class AuthViewSetTestCase(APITestCase):
    def test_login_1(self):
        self.user = User.objects.create_user(
            username="username",
            password="password",
        )

        response = self.api.post(
            path="/api/auth/login/",
            data={
                "username": "username",
                "password": "password",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data,
        )

    def test_refresh_1(self):
        self.user = User.objects.create_user(
            username="username",
            password="password",
        )

        response = self.api.post(
            path="/api/auth/login/",
            data={
                "username": "username",
                "password": "password",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data,
        )

        response = self.api.post(
            path="/api/auth/refresh/",
            data={
                "refresh": response.data["refresh"],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data,
        )
