from rest_framework import serializers
from users.serializers import UserSerializer
from blogs.models import Blog
from .models import Notification


class NotificationBlogSerializer(serializers.ModelSerializer):
    """Simplified blog serializer for notifications."""
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug']


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    blog = NotificationBlogSerializer(read_only=True)
    message = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'sender', 'receiver', 'type', 
            'blog', 'comment', 'is_read', 'message', 'created_at'
        ]
        read_only_fields = ['id', 'sender', 'receiver', 'type', 'blog', 'comment', 'created_at']

    def get_message(self, obj):
        if obj.type == Notification.NotificationType.LIKE:
            return f"{obj.sender.username} liked your blog '{obj.blog.title}'"
        elif obj.type == Notification.NotificationType.COMMENT:
            return f"{obj.sender.username} commented on your blog '{obj.blog.title}'"
        return ""
