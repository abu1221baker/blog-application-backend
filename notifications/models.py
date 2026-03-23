from django.conf import settings
from django.db import models


class Notification(models.Model):
    """
    Notification model to track user interactions like likes and comments.
    """

    class NotificationType(models.TextChoices):
        LIKE = 'LIKE', 'Like'
        COMMENT = 'COMMENT', 'Comment'

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    type = models.CharField(
        max_length=10,
        choices=NotificationType.choices,
    )
    blog = models.ForeignKey(
        'blogs.Blog',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
    )
    comment = models.ForeignKey(
        'comments.Comment',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f'{self.sender.username} {self.type} {self.receiver.username}'
