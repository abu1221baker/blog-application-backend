"""
Custom User and UserProfile models.

User extends AbstractUser with email as a required field.
UserProfile holds extended profile info and social links.
"""

import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


def avatar_upload_path(instance, filename):
    """Generate unique upload path for user avatars."""
    ext = filename.rsplit('.', 1)[-1].lower()
    return f'avatars/{instance.user.id}/{uuid.uuid4().hex}.{ext}'


class User(AbstractUser):
    """Custom user model with required email."""

    email = models.EmailField('email address', unique=True)

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """
    Extended profile information for a User.

    Created automatically via post_save signal.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    bio = models.TextField(max_length=500, blank=True, default='')
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    github = models.URLField(max_length=200, blank=True, default='')
    facebook = models.URLField(max_length=200, blank=True, default='')
    linkedin = models.URLField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'Profile of {self.user.username}'
class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
    )
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'followed'], name='unique_follow'
            )
        ]
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'

    def __str__(self):
        return f"{self.follower} follows {self.followed}"
