from django.test import TestCase as DjangoTestCase
from rest_framework.test import APITestCase as DRFAPITestCase


class BaseTestCase(DjangoTestCase):
    pass


class APITestCase(DRFAPITestCase, BaseTestCase):
    def setUp(self):
        super().setUp()

        self.api = self.client
        self.client = None
