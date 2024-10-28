# Generated by Django 4.2 on 2024-10-28 00:03

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Follower",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "follower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followers",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="follower",
                    ),
                ),
                (
                    "following",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followings",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="following",
                    ),
                ),
            ],
            options={
                "verbose_name": "Follower",
                "verbose_name_plural": "Followers",
                "ordering": ["-created_at"],
                "unique_together": {("following", "follower")},
            },
        ),
    ]
