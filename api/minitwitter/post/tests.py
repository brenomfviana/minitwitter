from common.test_utils.setup import APITestCase
from common.test_utils.steps import given_a_post, given_a_user
from rest_framework import status

from post.models import Like, Post


class PostTestCase(APITestCase):
    def test_create_1(self):
        user1 = given_a_user()

        self.assertEqual(Post.objects.count(), 0)

        data = {
            "text": "post content",
        }

        response = self.api.post(
            path="/api/posts/",
            data=data,
            **self.login(user=user1),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response,
        )

        self.assertEqual(Post.objects.count(), 1)

    def test_update_1(self):
        user1 = given_a_user()
        post1 = given_a_post(user=user1)

        data = {
            "text": "post content 2",
        }

        response = self.api.put(
            path=f"/api/posts/{post1.id}/",
            data=data,
            **self.login(user=user1),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response,
        )

        self.assertEqual(
            response.data,
            {
                "id": str(post1.id),
                "text": "post content 2",
                "user_username": user1.username,
                "user_name": user1.name,
            },
        )

    def test_delete_1(self):
        user1 = given_a_user()
        post1 = given_a_post(user=user1)

        self.assertEqual(Post.objects.count(), 1)

        response = self.api.delete(
            path=f"/api/posts/{post1.id}/",
            **self.login(user=user1),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response,
        )

        self.assertEqual(Post.objects.count(), 0)

    def test_like_1(self):
        user1 = given_a_user()
        post1 = given_a_post()

        self.assertEqual(Like.objects.count(), 0)

        response = self.api.patch(
            path=f"/api/posts/{post1.id}/like/",
            **self.login(user=user1),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            response,
        )

        self.assertEqual(Like.objects.count(), 1)

    def test_unlike_1(self):
        user1 = given_a_user()
        post1 = given_a_post(likers=[user1])

        self.assertEqual(Like.objects.count(), 1)

        response = self.api.patch(
            path=f"/api/posts/{post1.id}/unlike/",
            **self.login(user=user1),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            response,
        )

        self.assertEqual(Like.objects.count(), 0)
