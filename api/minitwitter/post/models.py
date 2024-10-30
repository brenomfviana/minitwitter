from common.models import BaseModel
from django.db import models
from user.models import User


class Post(BaseModel):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    text = models.CharField(
        verbose_name="post content",
        max_length=128,
    )
    is_reply = models.BooleanField(
        verbose_name="is reply?",
        default=False,
    )
    parent = models.ForeignKey(
        "post.Post",
        on_delete=models.DO_NOTHING,
        related_name="posts",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return f"Post ({self.id})"


class Like(BaseModel):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    class Meta:
        unique_together = ("user", "post")
        ordering = ["-created_at"]
        verbose_name = "like"
        verbose_name_plural = "likes"

    def __str__(self):
        return f"User {self.user.username} likes Post {self.post.id}"
