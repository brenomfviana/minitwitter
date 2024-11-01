# Generated by Django 4.2 on 2024-11-01 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0002_like"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="images",
                verbose_name="post image",
            ),
        ),
    ]
