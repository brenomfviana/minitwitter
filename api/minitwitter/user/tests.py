from common.test_utils import BaseTestCase
from rest_framework import status


class UserViewSetTestCase(BaseTestCase):
    def test_create_user_1(self):
        data = {
            "username": "username",
            "password": "password",
            "email": "user@email.com",
            "name": "User",
        }

        response = self.api.post(path="/api/users/", data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.data,
        )
