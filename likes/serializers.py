"""
Serializer for the Like model.
"""

from rest_framework import serializers

from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for likes. Read-only as creation is handled via custom view method."""

    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'blog', 'user', 'username', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
