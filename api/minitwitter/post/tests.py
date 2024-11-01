from time import sleep

from common.test_utils.setup import APITestCase
from common.test_utils.steps import given_a_post, given_a_user
from django.test import tag
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

        post1 = Post.objects.last()
        self.assertEqual(
            response.data,
            {
                "id": str(post1.id),
                "text": "post content",
                "user_username": user1.username,
                "user_name": user1.name,
                "like_count": post1.like_count,
            },
            response.data,
        )

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
                "like_count": post1.like_count,
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

    def test_reply_1(self):
        user1 = given_a_user()
        post1 = given_a_post(likers=[user1])

        self.assertEqual(Post.objects.count(), 1)

        data = {
            "text": "reply post",
        }

        response = self.api.post(
            path=f"/api/posts/{post1.id}/reply/",
            data=data,
            **self.login(user=user1),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response,
        )

        self.assertEqual(Post.objects.count(), 2)

        post2 = Post.objects.first()  # the most recent post is the first one
        self.assertEqual(
            response.data,
            {
                "id": str(post2.id),
                "text": "reply post",
                "user_username": user1.username,
                "user_name": user1.name,
                "like_count": post2.like_count,
            },
            response.data,
        )


class FeedTestCase(APITestCase):
    def test_feed_1(self):
        user1 = given_a_user()
        user2 = given_a_user(followers=[user1])
        user3 = given_a_user(followers=[user1, user2])

        post1 = given_a_post(
            user=user2,
            text="only user1 can see",
        )
        post2 = given_a_post(
            user=user3,
            text="both user1 and user 2 can see",
        )

        # user1's feed

        response = self.api.get(
            path="/api/feed/",
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
                "count": 2,
                "previous": None,
                "next": None,
                "results": [
                    {
                        "id": str(post2.id),
                        "text": "both user1 and user 2 can see",
                        "user_username": post2.user.username,
                        "user_name": post2.user.name,
                        "like_count": post2.like_count,
                    },
                    {
                        "id": str(post1.id),
                        "text": "only user1 can see",
                        "user_username": post1.user.username,
                        "user_name": post1.user.name,
                        "like_count": post1.like_count,
                    },
                ],
            },
            response.data,
        )

        # user2's feed

        response = self.api.get(
            path="/api/feed/",
            **self.login(user=user2),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response,
        )

        self.assertDictEqual(
            response.data,
            {
                "count": 1,
                "previous": None,
                "next": None,
                "results": [
                    {
                        "id": str(post2.id),
                        "text": "both user1 and user 2 can see",
                        "user_username": post2.user.username,
                        "user_name": post2.user.name,
                        "like_count": post2.like_count,
                    },
                ],
            },
            response.data,
        )

    @tag("slow", "integration")
    def test_feed_2_cache(self):
        user1 = given_a_user()
        user2 = given_a_user(followers=[user1])

        given_a_post(
            user=user2,
            text="user2's post 1",
        )

        credentials = self.login(user=user1)

        response = self.api.get(
            path="/api/feed/",
            **credentials,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response,
        )

        self.assertEqual(
            response.data.get("count"),
            1,
            response.data,
        )

        #

        given_a_post(
            user=user2,
            text="user2's post 2",
        )

        response = self.api.get(
            path="/api/feed/",
            **credentials,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response,
        )

        self.assertEqual(
            response.data.get("count"),
            1,
            response.data,
        )

        #

        sleep(120)  # wait Redis container

        response = self.api.get(
            path="/api/feed/",
            **credentials,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response,
        )

        self.assertEqual(
            response.data.get("count"),
            2,
            response.data,
        )
