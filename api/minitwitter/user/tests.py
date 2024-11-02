from unittest.mock import patch

from common.test_utils.setup import APITestCase
from common.test_utils.steps import given_a_user
from rest_framework import status

from user.models import Follower


class UserTestCase(APITestCase):
    def test_create_user_1_success(self):
        data = {
            "username": "username",
            "password": "password",
            "email": "user@email.com",
            "name": "User",
        }

        response = self.api.post(
            path="/api/users/",
            data=data,
        )

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
        self.assertEqual(
            response.data["email"],
            data["email"],
            response.data,
        )
        self.assertEqual(
            response.data["username"],
            data["username"],
            response.data,
        )
        self.assertEqual(
            response.data["name"],
            data["name"],
            response.data,
        )

    def test_create_user_2_invalid_email(self):
        data = {
            "username": "username",
            "password": "password",
            "email": "user@email",
            "name": "User",
        }

        response = self.api.post(
            path="/api/users/",
            data=data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            response,
        )
        self.assertDictEqual(
            response.data,
            {
                "email": ["Enter a valid email address."],
            },
            response.data,
        )

    def test_profile_1(self):
        user1 = given_a_user()
        user2 = given_a_user(followers=[user1])

        response = self.api.get(
            path=f"/api/users/{user2.id}/profile/",
            **self.login(user=user1),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response,
        )

        self.assertDictEqual(
            response.data,
            {
                "id": str(user2.id),
                "email": user2.email,
                "username": user2.username,
                "name": user2.name,
                "followers_count": user2.followers_count,
                "following_count": user2.following_count,
            },
            response.data,
        )


class FollowerTestCase(APITestCase):
    def test_follow_1_success(self):
        user1 = given_a_user()
        user2 = given_a_user()

        self.assertEqual(Follower.objects.count(), 0)

        with patch(
            "common.notifications.EmailService.send"
        ) as mocked_send_email:
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
        self.assertEqual(mocked_send_email.apply_async.call_count, 1)

    def test_follow_2_invalid_user(self):
        user1 = given_a_user()

        self.assertEqual(Follower.objects.count(), 0)

        invalid_id = "224f5c75-03d7-4e1b-9445-caa67ac80143"
        response = self.api.patch(
            path=f"/api/users/{invalid_id}/follow/",
            **self.login(user=user1),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            response,
        )
        self.assertDictEqual(
            response.data,
            {
                "error": "User not found!",
            },
            response.data,
        )

        self.assertEqual(Follower.objects.count(), 0)

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

    def test_unfollow_2_invalid_user(self):
        user1 = given_a_user()
        given_a_user(followers=[user1])

        self.assertEqual(Follower.objects.count(), 1)

        invalid_id = "224f5c75-03d7-4e1b-9445-caa67ac80143"
        response = self.api.patch(
            path=f"/api/users/{invalid_id}/unfollow/",
            **self.login(user=user1),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            response,
        )
        self.assertDictEqual(
            response.data,
            {
                "error": "User not found!",
            },
            response.data,
        )

        self.assertEqual(Follower.objects.count(), 1)
