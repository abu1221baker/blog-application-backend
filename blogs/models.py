"""
Blog and BlogContent models.

Blog stores only metadata (title, slug, hero banner, etc.).
BlogContent stores dynamic, ordered content blocks (text or image).
"""

import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def hero_banner_upload_path(instance, filename):
    """Generate unique upload path for blog hero banners."""
    ext = filename.rsplit('.', 1)[-1].lower()
    return f'blogs/heroes/{instance.id or "new"}/{uuid.uuid4().hex}.{ext}'


def content_image_upload_path(instance, filename):
    """Generate unique upload path for blog content images."""
    ext = filename.rsplit('.', 1)[-1].lower()
    blog_id = instance.blog_id or 'new'
    return f'blogs/content/{blog_id}/{uuid.uuid4().hex}.{ext}'


class Blog(models.Model):
    """
    Blog metadata model.

    Content is stored in separate BlogContent blocks — NOT in this model.
    This design enables dynamic, flexible blog layouts.
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blogs',
    )
    hero_banner = models.ImageField(
        upload_to=hero_banner_upload_path,
        blank=True,
        null=True,
    )
    hero_title = models.CharField(max_length=255, blank=True, default='')
    hero_subtitle = models.CharField(max_length=500, blank=True, default='')
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    viewed_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='viewed_blogs',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['slug']),
            models.Index(fields=['is_published', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate unique slug from title if not set."""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class BlogContent(models.Model):
    """
    Dynamic content block for a blog.

    Each block is either 'text' or 'image', ordered by the `order` field.
    A blog can have unlimited content blocks in any sequence.
    """

    class ContentType(models.TextChoices):
        TEXT = 'text', 'Text'
        IMAGE = 'image', 'Image'

    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='contents',
    )
    content_type = models.CharField(
        max_length=10,
        choices=ContentType.choices,
    )
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to=content_image_upload_path,
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Blog Content Block'
        verbose_name_plural = 'Blog Content Blocks'

    def __str__(self):
        return f'{self.blog.title} - {self.content_type} (#{self.order})'
