"""
Tests for Blogs app models and serializers.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from blogs.models import Blog, BlogContent
from blogs.serializers import BlogContentSerializer

User = get_user_model()


class BlogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Password123!',
        )
        self.blog = Blog.objects.create(
            title='Test Blog Post',
            author=self.user,
        )

    def test_slug_auto_generation(self):
        """Test that slug is automatically generated from title."""
        self.assertEqual(self.blog.slug, 'test-blog-post')

    def test_unique_slug(self):
        """Test that duplicate titles get unique slugs."""
        blog2 = Blog.objects.create(
            title='Test Blog Post',
            author=self.user,
        )
        self.assertEqual(blog2.slug, 'test-blog-post-1')


class BlogContentValidationTest(TestCase):
    def test_text_block_valid(self):
        data = {
            'content_type': 'text',
            'text': 'This is some text.',
        }
        serializer = BlogContentSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_text_block_missing_text(self):
        data = {
            'content_type': 'text',
        }
        serializer = BlogContentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('text', serializer.errors)

    def test_text_block_with_image(self):
        # We simulate an image file using simple data here since DRF serializers
        # process files via multi-part parsing, but this checks the dict logic.
        data = {
            'content_type': 'text',
            'text': 'Text here',
            'image': 'dummy_image.jpg',
        }
        serializer = BlogContentSerializer(data=data)
        # Validation fails since image is provided for text block
        self.assertFalse(serializer.is_valid())
        self.assertIn('image', serializer.errors)
