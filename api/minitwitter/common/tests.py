from rest_framework import status

from common.test_utils.setup import APITestCase
from common.test_utils.steps import given_a_user


class TrottleTestCase(APITestCase):
    def test_throttle_anonym_1_create_user(self):
        max_throttle = 1
        for i in range(max_throttle + 1):
            data = {
                "username": f"username{i}",
                "password": f"password{i}",
                "email": f"user{i}@email.com",
                "name": f"User{i}",
            }

            response = self.api.post(
                path="/api/users/",
                data=data,
            )

            if i < max_throttle:
                self.assertEqual(
                    response.status_code,
                    status.HTTP_201_CREATED,
                    response,
                )
            else:
                self.assertEqual(
                    response.status_code,
                    status.HTTP_429_TOO_MANY_REQUESTS,
                    response,
                )

    def test_throttle_user_1_feed(self):
        user1 = given_a_user()

        credentials = self.login(user=user1)

        max_throttle = 10
        for i in range(max_throttle + 1):
            response = self.api.get(
                path="/api/feed/",
                **credentials,
            )

            if i < max_throttle:
                self.assertEqual(
                    response.status_code,
                    status.HTTP_200_OK,
                    response,
                )
            else:
                self.assertEqual(
                    response.status_code,
                    status.HTTP_429_TOO_MANY_REQUESTS,
                    response,
                )
