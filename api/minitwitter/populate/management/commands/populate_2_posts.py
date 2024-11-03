from common.test_utils.steps import given_a_post
from django.core.management import BaseCommand
from django.db.transaction import atomic
from user.models import Follower, User


class Command(BaseCommand):
    help = "Create posts"

    def handle(self, *args, **options):
        import logging

        logging.disable()

        with atomic():
            user1 = User.objects.get(username="testuser1")
            user1_followings = Follower.objects.filter(follower=user1)
            for user in user1_followings:
                given_a_post(user=user.following)

            user2 = User.objects.get(username="testuser2")
            user2_followings = Follower.objects.filter(follower=user2)
            for user in user2_followings:
                given_a_post(user=user.following)

        self.stdout.write(self.style.SUCCESS("Posts created!"))
