from django.core.management import BaseCommand
from django.db.transaction import atomic

from common.test_utils.steps import given_a_user


class Command(BaseCommand):
    help = "Create users"

    def handle(self, *args, **options):
        import logging

        logging.disable()

        with atomic():
            user1 = given_a_user(
                username="testuser1",
                email="testuser1@email.com",
                name="Test User 1",
            )
            for i in range(10):
                given_a_user(followers=[user1])

            user2 = given_a_user(
                username="testuser2",
                email="testuser2@email.com",
                name="Test User 2",
                followers=[user1],
            )
            for i in range(4):
                given_a_user(followers=[user2])

        self.stdout.write(self.style.SUCCESS("Users created!"))
