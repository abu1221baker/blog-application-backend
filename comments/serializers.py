"""
Serializers for comments with recursive nested children.
"""

from rest_framework import serializers

from .models import Comment


class RecursiveChildSerializer(serializers.Serializer):
    """Serializer that recursively serializes children."""

    def to_representation(self, instance):
        serializer = CommentSerializer(instance, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment serializer with recursive nested children.

    Includes read-only author info and child comments.
    """

    author_username = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    children = RecursiveChildSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'blog', 'author_id', 'author_username',
            'parent', 'body', 'children',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'author_id', 'author_username', 'created_at', 'updated_at']

    def validate_parent(self, value):
        """Ensure parent comment belongs to the same blog."""
        if value:
            blog_id = self.initial_data.get('blog') or (
                self.instance.blog_id if self.instance else None
            )
            if blog_id and value.blog_id != int(blog_id):
                raise serializers.ValidationError(
                    'Parent comment must belong to the same blog.'
                )
        return value
