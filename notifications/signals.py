from django.db.models.signals import post_save
from django.dispatch import receiver
from likes.models import Like
from comments.models import Comment
from .models import Notification


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    """Create notification when a blog is liked."""
    if created:
        # Avoid notifying yourself
        if instance.user != instance.blog.author:
            Notification.objects.create(
                sender=instance.user,
                receiver=instance.blog.author,
                type=Notification.NotificationType.LIKE,
                blog=instance.blog
            )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Create notification when a blog is commented on."""
    if created:
        # Avoid notifying yourself
        if instance.author != instance.blog.author:
            Notification.objects.create(
                sender=instance.author,
                receiver=instance.blog.author,
                type=Notification.NotificationType.COMMENT,
                blog=instance.blog,
                comment=instance
            )
