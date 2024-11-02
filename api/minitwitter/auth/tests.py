from time import sleep

from common.test_utils.setup import APITestCase
from common.test_utils.steps import given_a_user
from rest_framework import status


class AuthViewSetTestCase(APITestCase):
    def test_login_1(self):
        given_a_user(
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
        given_a_user(
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

        sleep(1)  # wait Redis container (throttle uses Redis cache)

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
