"""
Like model.
"""

from django.conf import settings
from django.db import models


class Like(models.Model):
    """
    Records a user liking a specific blog post.

    Uses unique_together to prevent a user from liking
    the same post multiple times.
    """

    blog = models.ForeignKey(
        'blogs.Blog',
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        # Prevent duplicate likes
        constraints = [
            models.UniqueConstraint(
                fields=['blog', 'user'], name='unique_blog_user_like'
            )
        ]

    def __str__(self):
        return f'{self.user.username} liked {self.blog.title}'
