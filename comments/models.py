"""
Comment model with nested/threaded comments support.
"""

from django.conf import settings
from django.db import models


class Comment(models.Model):
    """
    Comment on a blog post.

    Supports nested comments via self-referencing `parent` field.
    """

    blog = models.ForeignKey(
        'blogs.Blog',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )
    body = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        indexes = [
            models.Index(fields=['blog', 'created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog.title}'

    @property
    def is_reply(self):
        return self.parent is not None
