from django.test import TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.api = self.client
        self.client = None
