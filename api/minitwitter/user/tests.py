from common.test_utils.setup import APITestCase
from common.test_utils.steps import given_a_user
from rest_framework import status

from user.models import Follower


class UserViewSetTestCase(APITestCase):
    def test_create_user_1(self):
        data = {
            "username": "username",
            "password": "password",
            "email": "user@email.com",
            "name": "User",
        }

        response = self.api.post(path="/api/users/", data=data,)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response,
        )

        self.assertIn(
            "id",
            response.data,
            response.data,
        )
        self.assertEquals(
            data["email"],
            response.data["email"],
            response.data,
        )
        self.assertEquals(
            data["username"],
            response.data["username"],
            response.data,
        )
        self.assertEquals(
            data["name"],
            response.data["name"],
            response.data,
        )

    def test_follow_1(self):
        user1 = given_a_user()
        user2 = given_a_user()

        self.assertEqual(Follower.objects.count(), 0)

        response = self.api.patch(
            path=f"/api/users/{user2.id}/follow/",
            **self.login(user=user1),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            response,
        )

        self.assertEqual(Follower.objects.count(), 1)

    def test_unfollow_1(self):
        user1 = given_a_user()
        user2 = given_a_user(followers=[user1])

        self.assertEqual(Follower.objects.count(), 1)

        response = self.api.patch(
            path=f"/api/users/{user2.id}/unfollow/",
            **self.login(user=user1),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            response,
        )

        self.assertEqual(Follower.objects.count(), 0)
