from unittest.mock import PropertyMock, patch

from django.core.cache import cache
from django.test import TestCase as DjangoTestCase
from rest_framework.test import APITestCase as DRFAPITestCase
from user.models import User

from common.test_utils.factories import DEFAULT_PASSWORD


class BaseTestCase(DjangoTestCase):
    def setUp(self):
        super().setUp()

        self.celery_task_always_eager_patcher = patch(
            "minitwitter.celery.CeleryConfig.task_always_eager",
            new_callable=PropertyMock,
            return_value=True,
        )
        self.celery_task_eager_propagates_patcher = patch(
            "minitwitter.celery.CeleryConfig.task_eager_propagates",
            new_callable=PropertyMock,
            return_value=True,
        )

        self.mocked_celery_task_always_eager = (
            self.celery_task_always_eager_patcher.start(),
        )
        self.mocked_celery_task_eager_propagates = (
            self.celery_task_eager_propagates_patcher.start(),
        )

        self.addCleanup(self.celery_task_always_eager_patcher.stop)
        self.addCleanup(self.celery_task_eager_propagates_patcher.stop)


class APITestCase(DRFAPITestCase, BaseTestCase):
    def setUp(self):
        super().setUp()

        self.api = self.client
        self.client = None
        self.last_login = None

    def tearDown(self):
        self.last_login = None
        cache.clear()

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
        return {
            "HTTP_AUTHORIZATION": f"Bearer {access_token}",
        }
