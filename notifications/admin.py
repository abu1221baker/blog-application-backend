from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'type', 'blog', 'is_read', 'created_at']
    list_filter = ['type', 'is_read', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'blog__title']
    readonly_fields = ['created_at']
