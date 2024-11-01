from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from post.models import Post


@receiver(post_save, sender=Post)
@receiver(post_delete, sender=Post)
def clear_feed_cache(sender, instance, **kwargs):
    pattern = f"user_feed_{instance.user.id}_page_*"
    cache.delete(cache.keys(pattern))
