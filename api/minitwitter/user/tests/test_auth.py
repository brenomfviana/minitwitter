from common.test_utils import BaseTestCase
from django.urls import reverse
from rest_framework import status
from user.models import User


class AuthTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_auth_1(self):
        url = reverse('token_obtain_pair')

        data = {
            "username": "testuser",
            "password": "testpass",
        }

        response = self.api.post(path=url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
