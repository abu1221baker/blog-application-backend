"""
Serializers for Blog and BlogContent models.

Supports nested author profile, ordered content blocks,
and content_type-based validation.
"""

from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Blog, BlogContent


class BlogContentSerializer(serializers.ModelSerializer):
    """
    Serializer for dynamic blog content blocks.

    Validates that text blocks have text and image blocks have an image.
    """

    class Meta:
        model = BlogContent
        fields = ['id', 'content_type', 'text', 'image', 'order']

    def validate(self, attrs):
        content_type = attrs.get('content_type')
        text = attrs.get('text')
        image = attrs.get('image')

        if content_type == BlogContent.ContentType.TEXT:
            if not text:
                raise serializers.ValidationError(
                    {'text': 'Text content is required for text blocks.'}
                )
            if image:
                raise serializers.ValidationError(
                    {'image': 'Image should not be provided for text blocks.'}
                )
        elif content_type == BlogContent.ContentType.IMAGE:
            if not image:
                raise serializers.ValidationError(
                    {'image': 'Image is required for image blocks.'}
                )
            if text:
                raise serializers.ValidationError(
                    {'text': 'Text should not be provided for image blocks.'}
                )

        return attrs


class BlogListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for blog list views."""

    author = UserSerializer(read_only=True)
    content_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'author', 'hero_banner',
            'hero_title', 'hero_subtitle', 'is_published', 'views_count',
            'content_count', 'like_count', 'created_at', 'updated_at',
        ]

    def get_content_count(self, obj):
        return obj.contents.count()

    def get_like_count(self, obj):
        return obj.likes.count() if hasattr(obj, 'likes') else 0


class BlogDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for blog detail views.

    Includes nested author profile and ordered content blocks.
    """

    author = UserSerializer(read_only=True)
    contents = BlogContentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'author', 'hero_banner',
            'hero_title', 'hero_subtitle', 'is_published', 'views_count',
            'contents', 'like_count', 'is_liked',
            'created_at', 'updated_at',
        ]

    def get_like_count(self, obj):
        return obj.likes.count() if hasattr(obj, 'likes') else 0

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating blogs.

    Slug is auto-generated from title if not provided.
    """

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'hero_banner',
            'hero_title', 'hero_subtitle', 'is_published',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
